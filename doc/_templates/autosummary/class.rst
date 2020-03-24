{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

.. rubric:: Methods Summary

.. autosummary::
    {% for item in methods %}
    {% if item != '__init__' %}
    {{ objname }}.{{ item }}
    {% endif %}
    {% endfor %}

.. include:: backreferences/{{ fullname }}.examples

.. raw:: html

     <div style='clear:both'></div>

