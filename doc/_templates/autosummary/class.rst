{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

{% block methods_documentation %}
{% if methods %}

.. raw:: html

    <hr>

Methods Documentation
---------------------

{% for item in methods %}
{% if item != '__init__' %}
.. automethod:: {{ objname }}.{{ item }}
{% endif %}
{% endfor %}

{% endif %}
{% endblock %}

.. raw:: html

     <div style='clear:both'></div>

