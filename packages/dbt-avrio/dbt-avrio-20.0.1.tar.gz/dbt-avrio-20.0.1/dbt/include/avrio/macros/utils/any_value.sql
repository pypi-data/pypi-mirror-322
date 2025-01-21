{% macro avrio__any_value(expression) -%}
    min({{ expression }})
{%- endmacro %}
