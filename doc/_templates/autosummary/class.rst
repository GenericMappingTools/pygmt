{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

{% if attributes %}
.. rubric:: Attributes

{% for item in attributes %}
.. autoproperty::
    {{ objname }}.{{ item }}
{% endfor %}
{% endif %}

{% if methods != ["__init__"] %}
.. rubric:: Methods Summary

.. autosummary::
    {% for item in methods %}
    {% if item != '__init__' %}
    {{ objname }}.{{ item }}
    {% endif %}
    {% endfor %}
{% endif %}

.. include:: backreferences/{{ fullname }}.examples

.. raw:: html

     <div style='clear:both'></div>

