{%- block front_matter -%}
---
category: RELEASE
id: RELEASE-001
revision: 1
title: Release {{ system.release_id }} Summary
manufacturer_name: {{ system.manufacturer_name }}
---
{%- endblock %}
{% block purpose %}
# Purpose

The purpose of this document is to list the change requests that were implemented within the current release.  It also includes approval of the change requests and the verification of the implemented changes.  Finally, it lists the problem reports that were addressed in the release as well as any outstanding problem reports (i.e., known anomalies).

# Scope

The scope of this document is the software system within the {{ system.project_name }} product.  It includes changes made within {{ system.release_id }}.
{%- endblock %}
{% block definitions %}
{%- endblock %}
{% block change_requests %}
# Change Requests
{% for cr in change_requests %}
## {% if cr.status == 'open' %}(OPEN) {% endif %}{{ cr.title }}

**Identifier:** {{ cr.id }}

**Description:**

{{ cr.content }}
{% endfor %}
{%- endblock %}
{% block problem_reports %}
# Problem Reports
{% for pr in problem_reports %}
## {% if pr.status == 'open' %}(OPEN) {% endif %}{{ pr.title }}

**Identifier:** {{ pr.id }}

**Description:**

{{ pr.content }}
{% endfor %}
{%- endblock %}