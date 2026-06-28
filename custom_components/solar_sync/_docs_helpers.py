_B='Description'
_A=None
from typing import Any
import homeassistant.helpers.config_validation as cv,pandas as pd,voluptuous as vol
from homeassistant.helpers import selector
from.const import DOCS,DOCS_APPLY,DOCS_MANUAL_CONTROL,SET_MANUAL_CONTROL_SCHEMA,VALIDATION_TUPLES,apply_service_schema
def _format_voluptuous_instance(instance):
	A=_A;B=_A;C=_A
	for D in instance.validators:
		if isinstance(D,vol.Coerce):A=D.type.__name__
		elif isinstance(D,vol.Clamp|vol.Range):B=D.min;C=D.max
	if B is not _A and C is not _A:return f"`{A}` {B}-{C}"
	if B is not _A:return f"`{A} > {B}`"
	if C is not _A:return f"`{A} < {C}`"
	return f"`{A}`"
def _type_to_str(type_):
	A=type_
	if A==cv.entity_ids:return'list of `entity_id`s'
	if A in(bool,int,float,str):return f"`{A.__name__}`"
	if A==cv.boolean:return'bool'
	if isinstance(A,vol.All):return _format_voluptuous_instance(A)
	if isinstance(A,vol.Any):return' or '.join(_type_to_str(A)for A in A.validators)
	if isinstance(A,vol.In):return f"one of `{A.container}`"
	if isinstance(A,selector.SelectSelector):return f"one of `{A.config["options"]}`"
	if isinstance(A,selector.ColorRGBSelector):return'RGB color'
	B=f"Unknown type: {A}";raise ValueError(B)
def generate_config_markdown_table():
	A=[]
	for(B,C,D)in VALIDATION_TUPLES:E=DOCS[B];F={'Variable name':f"`{B}`",_B:E,'Default':f"`{C}`",'Type':_type_to_str(D)};A.append(F)
	G=pd.DataFrame(A);return G.to_markdown(index=False)
def _schema_to_dict(schema):
	B={}
	for(A,C)in schema.schema.items():
		if isinstance(A,vol.Optional):D=A.default;B[A.schema]=D,C
	return B
def _generate_service_markdown_table(schema,alternative_docs=_A):
	C=alternative_docs;B=schema;F=_schema_to_dict(B)if isinstance(B,vol.Schema)else B;D=[]
	for(A,(G,H))in F.items():
		if C is not _A and A in C:E=C[A]
		else:E=DOCS[A]
		I={'Service data attribute':f"`{A}`",_B:E,'Required':'✅'if G==vol.UNDEFINED else'❌','Type':_type_to_str(H)};D.append(I)
	J=pd.DataFrame(D);return J.to_markdown(index=False)
def generate_apply_markdown_table():return _generate_service_markdown_table(apply_service_schema(),DOCS_APPLY)
def generate_set_manual_control_markdown_table():return _generate_service_markdown_table(SET_MANUAL_CONTROL_SCHEMA,DOCS_MANUAL_CONTROL)