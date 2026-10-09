{#- Cross-database helpers: every model runs unchanged on DuckDB (local) and Snowflake. -#}
{% macro jfield(col, path, type='varchar') -%}{{ return(adapter.dispatch('jfield')(col, path, type)) }}{%- endmacro %}
{% macro duckdb__jfield(col, path, type) -%}try_cast(json_extract_string({{ col }}, '$.{{ path }}') as {{ type }}){%- endmacro %}
{% macro snowflake__jfield(col, path, type) -%}try_cast({{ col }}:{{ path }}::varchar as {{ type }}){%- endmacro %}

{% macro json_array_length(col, path) -%}{{ return(adapter.dispatch('json_array_length')(col, path)) }}{%- endmacro %}
{% macro duckdb__json_array_length(col, path) -%}json_array_length({{ col }}, '$.{{ path }}'){%- endmacro %}
{% macro snowflake__json_array_length(col, path) -%}array_size({{ col }}:{{ path }}){%- endmacro %}

{% macro pctl(col, p) -%}{{ return(adapter.dispatch('pctl')(col, p)) }}{%- endmacro %}
{% macro duckdb__pctl(col, p) -%}quantile_cont({{ col }}, {{ p }}){%- endmacro %}
{% macro snowflake__pctl(col, p) -%}percentile_cont({{ p }}) within group (order by {{ col }}){%- endmacro %}
