The ``{{ fullname }}`` module
{% for i in range(fullname|length + 15) %}={% endfor %}

.. automodule:: {{ fullname }}

{% block classes %}
{% if classes %}
.. rubric:: Classes

.. autosummary::
  :toctree: ./
{% for item in classes %}
  {{ item }}
{% endfor %}
{% endif %}
{% endblock %}


{% block functions %}
{% if functions %}
.. rubric:: Functions

.. autosummary::
  :toctree: ./
{% for item in functions %}
  {{ item }}
{% endfor %}
{% endif %}
{% endblock %}


{% block exceptions %}
{% if exceptions %}
.. rubric:: Exceptions

.. autosummary::
  :toctree: ./
{% for item in exceptions %}
  {{ item }}
{% endfor %}
{% endif %}
{% endblock %}
