{% macro avrio__current_timestamp() -%}
    current_timestamp
{%- endmacro %}

{% macro avrio__snapshot_string_as_time(timestamp) %}
    {%- set result = "timestamp '" ~ timestamp ~ "'" -%}
    {{ return(result) }}
{% endmacro %}
