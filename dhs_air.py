#!/usr/bin/python

import sys
import cgi
import traceback
import StringIO
import urllib
import re

from tmswap import policyrunner
from tmswap import llyn
from tmswap.RDFSink import SUBJ, PRED, OBJ
from tmswap import uripath

import render_law

_filter_properties = [
    'http://dig.csail.mit.edu/TAMI/2007/amord/air#compliant-with',
    'http://dig.csail.mit.edu/TAMI/2007/amord/air#non-compliant-with']

_log_boilerplate = """
@prefix : <http://dig.csail.mit.edu/2012/DHS/JHU/common/fusion_ONT#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
"""

_transaction_uri = ("http://dig.csail.mit.edu/2012/DHS/JHU/common/"
                    "fusion_ONT#Transaction")

_subjective_form_boilerplate = """
<html>
<head>
    <link type="text/css" href="css/custom.css" rel="stylesheet" />
</head>
<body>

<table>
    <tr>
        <td>Transaction sender:</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Transaction receiver:</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Transaction file:</td>
        <td>%s</td>
    </tr>
<table>

<form name="subjective_questions" action="dhs_air.py" method="get">

<input type="hidden" name="subjectives" value="true" />

%s

<br/>
<table>
%s
</table>

<br/>
<input type="submit" value="Submit" />
</form>
</body>
</html>
"""

_xmp_parser = "http://dice.csail.mit.edu/xmpparser.py"

_store = llyn.RDFStore()

_rdfs_prefix = "http://www.w3.org/2000/01/rdf-schema"
_air_prefix = "http://dig.csail.mit.edu/TAMI/2007/amord/air"
_fusion_prefix = "http://dig.csail.mit.edu/2012/DHS/JHU/common/fusion_ONT"

_see_also_predicate = "%s#seeAlso" % _rdfs_prefix
_label_predicate = "%s#label" % _rdfs_prefix

_transaction_predicate = "%s#transaction_ontology" % _fusion_prefix

_air_description = "%s#description" % _air_prefix
_air_statement = "%s#statement" % _air_prefix

_subjective_object = "%s#Subjective" % _air_prefix
_subjective_term_predicate = "%s#subjective_term" % _air_prefix
_subjective_term_sender = "%s#Sender" % _air_prefix
_subjective_term_receiver = "%s#Receiver" % _air_prefix
_subjective_term_data = "%s#Data" % _air_prefix
_subjective_term_transaction = "%s#Transaction" % _air_prefix

# fast stable uniqueify
def uniqueify(seq):
    seen = {}
    result = []
    for item in seq:
        if item in seen:
            continue
        seen[item] = 1
        result.append(item)
    return result

def url_to_context(url):
    context = _store.load(uripath.splitFrag(url)[0],
                          remember = 0, referer = '', topLevel = True)
    context.reopen()
    context.stayOpen = 1
    return context

def get_subjective_terms(context):
    term_dict = {}
    subjective_term_pred = context.newSymbol(_subjective_term_predicate)
    subjective_bindings = context.statementsMatching(pred=subjective_term_pred)
    for elem in subjective_bindings:
        term_dict[elem[SUBJ]] = elem[OBJ]
    return term_dict

def get_subjective_rules(context):
    rule_dict = {}
    subjective_object = context.newSymbol(_subjective_object)
    subjective_rules = context.statementsMatching(obj=subjective_object)
    air_description = context.newSymbol(_air_description)
    air_statement = context.newSymbol(_air_statement)
    for elem in subjective_rules:
        rule_name = elem[SUBJ]
        descr = context.the(subj = rule_name, pred = air_description)
        triple = context.the(subj = rule_name, pred = air_statement)
        rule_dict[rule_name] = (descr, triple)
    return rule_dict

def render_subjective_form(term_dict, rule_dict, name_dict):
    output = []
    template = """
    <tr>
        <td><input type="checkbox" name="subjective" value="%s"/></td>
        <td>%s</td>
    </tr>"""
    for rule in sorted(rule_dict.keys()):
        tokens = []
        for token in rule_dict[rule][0]:
            if token in term_dict:
                assert term_dict[token] in name_dict
                tokens.append(name_dict[term_dict[token]])
            else:
                tokens.append(str(token))
        output.append(template % (rule, ''.join(tokens)))
    return ''.join(output)

def evaluate_seealso(context):
    see_also_pred = context.newSymbol(_see_also_predicate)
    see_alsos = context.statementsMatching(pred=see_also_pred)
    return [str(elem[OBJ]) for elem in see_alsos]

def get_transaction_ontology(context):
    transaction_pred = context.newSymbol(_transaction_predicate)
    transaction = context.statementsMatching(pred=transaction_pred)
    if not transaction:
        return None
    return str(transaction[0][OBJ])

def foaf_to_canonical_name(context):
    label_pred = context.newSymbol(_label_predicate)
    foaf_label = context.statementsMatching(pred=label_pred)
    if not foaf_label:
        return url
    return str(foaf_label[0][OBJ])

def generate_log(by_uri, to_uri, data_uri, policy_uri,
                 by_label = None, to_label = None, data_label = None):
    output_buffer = [_log_boilerplate]

    output_buffer.append("<%s> a <%s#Request>, <%s#Disseminate>;" %
        (_transaction_uri, policy_uri, policy_uri))
    output_buffer.append("    <%s#by> <%s>;" % (policy_uri, by_uri))
    output_buffer.append("    <%s#to> <%s>;" % (policy_uri, to_uri))
    output_buffer.append("    <%s#data> <%s>;" % (policy_uri, data_uri))
    output_buffer.append("    <%s#doc-data> <%s?uri=%s>.\n" % (
        policy_uri, _xmp_parser, data_uri))

    if by_label:
        output_buffer.append('<%s> <%s> "%s".' % (
            by_uri, _label_predicate, by_label))
    if to_label:
        output_buffer.append('<%s> <%s> "%s".' % (
            to_uri, _label_predicate, to_label))
    if data_label:
        output_buffer.append('<%s> <%s> "%s".' % (
            data_uri, _label_predicate, data_label))
    return '\n'.join(output_buffer)

def format_headers(content_type, content):
    output_buffer = []

    output_buffer.append("Content-type: %s\n" % content_type)
    output_buffer.append("Content-Length: %d\n" % len(content))
    output_buffer.append("\n")
    output_buffer.append(content)

    return ''.join(output_buffer)

def copy_params(form):
    hidden_template = '<input type="hidden" name="%s" value="%s" />\n'
    output_buffer = []
    for key in form.keys():
        for value in form.getlist(key):
            output_buffer.append(hidden_template % (key, value))
    return ''.join(output_buffer)

def get_subjective_html(form, subjective_zip, by_label,
                        to_label, data_label, transaction_label):
    elements = []
    for context, terms, rules in subjective_zip:
        sym_to_label = {
            context.newSymbol(_subjective_term_sender): by_label,
            context.newSymbol(_subjective_term_receiver): to_label,
            context.newSymbol(_subjective_term_data): data_label,
            context.newSymbol(_subjective_term_transaction): transaction_label,
            }
        elements.append(render_subjective_form(terms, rules, sym_to_label))
    return _subjective_form_boilerplate % (
        by_label, to_label, data_label, copy_params(form), ''.join(elements))

def get_subjective_log(subjective_zip, active_rule, by_uri, to_uri,
                       data_uri, transaction_uri):
    new_triples = []
    for context, terms, rules in subjective_zip:
        sym_mapping = {
            context.newSymbol(_subjective_term_sender): by_uri,
            context.newSymbol(_subjective_term_receiver): to_uri,
            context.newSymbol(_subjective_term_data): data_uri,
            context.newSymbol(_subjective_term_transaction): transaction_uri,
            }

        for rule in rules:
            if active_rule == str(rule):
                for triple in rules[rule][1]:
                    if triple[SUBJ] in terms:
                        subject = sym_mapping[terms[triple[SUBJ]]]
                    else:
                        subject = triple[SUBJ].uriref()

                    if triple[OBJ] in terms:
                        object = sym_mapping[terms[triple[OBJ]]]
                    else:
                        object = triple[OBJ].uriref()

                    new_triples.append("<%s> <%s> <%s>." % (
                        subject, triple[PRED].uriref(), object))
    return '\n'.join(new_triples)

def generate_output(form):
    log_uris = form.getlist('logFile')
    rule_uris = form.getlist('rulesFile')
    log = form.getfirst('log')
    rules = form.getfirst('rules')

    if not rule_uris:
        return ('text/plain', "No rules files specified!")

    rules_contexts = [url_to_context(elem) for elem in rule_uris]

    see_also = []
    for context in rules_contexts:
        see_also.extend(evaluate_seealso(context))

    by_uri = form.getfirst('by')
    to_uri = form.getfirst('to')
    data_uri = form.getfirst('data')

    if (by_uri and to_uri and data_uri):
        by_context = url_to_context(by_uri)
        to_context = url_to_context(to_uri)

        see_also.extend(evaluate_seealso(by_context))
        see_also.extend(evaluate_seealso(to_context))

        if form.getfirst('by_label'):
            by_label = form.getfirst('by_label')
        else:
            by_label = foaf_to_canonical_name(by_context)

        if form.getfirst('to_label'):
            to_label = form.getfirst('to_label')
        else:
            to_label = foaf_to_canonical_name(to_context)

        if form.getfirst('data_label'):
            data_label = form.getfirst('data_label')
        else:
            data_url = form.getfirst('data')
            rightmost_slash = data_url.rfind('/')
            if rightmost_slash != -1:
                data_label = data_url[rightmost_slash + 1:]
            else:
                data_label = data_url

        if form.getfirst('transaction_label'):
            transaction_label = form.getfirst('transaction_label')
        else:
            transaction_label = "Transaction"

        if form.getfirst('policy'):
            transaction_policy = form.getfirst('policy')
        else:
            transaction_policy = get_transaction_ontology(rules_contexts[0])

        log = generate_log(by_uri, to_uri, data_uri, transaction_policy,
                           by_label, to_label, data_label)

        subjective_terms = [get_subjective_terms(i) for i in rules_contexts]
        subjective_rules = [get_subjective_rules(i) for i in rules_contexts]
        subjective_zip = zip(rules_contexts, subjective_terms, subjective_rules)

        if any(subjective_rules):
            if form.getfirst("subjectives"):
                for active_rule in form.getlist("subjective"):
                    subjective_log = get_subjective_log(
                        subjective_zip, active_rule,
                        by_uri, to_uri, data_uri, _transaction_uri)
                    log = "%s\n%s" % (log, subjective_log)
            else:
                html_output = get_subjective_html(
                    form, subjective_zip, by_label,
                    to_label, data_label, transaction_label)
                return ('text/html', html_output)

    if form.getfirst('print_preprocessing'):
        output_str = []
        output_str.append("rdfs:seeAlso urls found (%d):\n\t%s" % (
            len(see_also), '\n\t'.join(see_also)))
        output_str.append("rdfs:transaction uri used:\n\t%s" % (
            transaction_policy))
        output_str.append("Canonical by: %s\nCanonical to: %s" % (
            by_label, to_label))
        output_str.append("\nGenerated log:\n%s" % log)
        return ('text/plain', '\n'.join(output_str))

    if form.getfirst('print_log'):
        return ('text/plain', log)

    log_uris.extend(see_also)
    log_uris = uniqueify(log_uris)

    reasoner_str = policyrunner.testPolicy(
        log_uris, rule_uris, log, rules, _filter_properties).encode('utf-8')
    if form.getfirst('use_tabulator') == 'true':
        if form.getfirst('debug'):
            header = 'text/plain'
        else:
            header = 'text/rdf+n3'
        return (header, reasoner_str)
    else:
        html_output = render_law.render_law(
            reasoner_str, 'uri_str', rule_uris[0])
        return ('text/html', html_output)

def main_wsgi():
    import wsgiref.handlers
    wsgiref.handlers.CGIHandler().run(wsgi_app)

def wsgi_app(environ, start_response):
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

    try:
        type, content = generate_output(form)
        start_response('200 OK', [('Content-Type', type),
                                  ('Content-Length', str(len(content)))])
        yield content
    except:
        error_log = ''.join(traceback.format_exception(
            sys.exc_type, sys.exc_value, sys.exc_traceback))
        start_response('500 Internal Server Error',
                       [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(error_log)))])
        yield error_log

def main():
    stdout_ptr = sys.stdout
    sys.stdout = StringIO.StringIO()
    form = cgi.FieldStorage()

    try:
        header, content = generate_output(form)
        stdout_ptr.write(format_headers(header, content))
    except:
        error_log = ''.join(traceback.format_exception(
            sys.exc_type, sys.exc_value, sys.exc_traceback))
        stdout_ptr.write(format_headers('text/plain', error_log))

if __name__ == "__main__":
    main()
