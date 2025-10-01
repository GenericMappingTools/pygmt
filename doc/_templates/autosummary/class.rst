{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

{% if '_aliases' not in attributes %}
.. rubric:: Attributes

{% for item in attributes %}
.. autoproperty::
    {{ objname }}.{{ item }}
{% endfor %}
{% endif %}

{% if methods != ["__init__"] %}
.. rubric:: Methods Summary

.. autosummary::
    :toctree:
    {% for item in methods %}
    {% if item != '__init__' %}
    {{ objname }}.{{ item }}
    {% endif %}
    {% endfor %}
{% endif %}

.. minigallery:: {{ fullname }}
    :add-heading:

.. raw:: html

     <div style='clear:both'></div>
