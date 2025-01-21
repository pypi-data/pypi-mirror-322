{% macro avrio__type_float() -%}
    double
{%- endmacro %}

{% macro avrio__type_string() -%}
    varchar
{%- endmacro %}

{% macro avrio__type_numeric() -%}
    decimal(28, 6)
{%- endmacro %}

{%- macro avrio__type_int() -%}
    integer
{%- endmacro -%}
