from __future__ import annotations
_AV='Unrecognized error-tag: '
_AU='partial-operation'
_AT='operation-failed'
_AS='rollback-failed'
_AR='data-exists'
_AQ='resource-denied'
_AP='lock-denied'
_AO='unknown-namespace'
_AN='bad-element'
_AM='unknown-attribute'
_AL='missing-attribute'
_AK='exception-thrown'
_AJ='functions'
_AI='function-details'
_AH='from-device'
_AG='identity-certificate'
_AF='source-ip-address'
_AE='serial-number'
_AD='/yangcore:dynamic-callouts/dynamic-callout='
_AC='"ietf-sztp-bootstrap-server:input" is missing.'
_AB='/ietf-sztp-bootstrap-server:report-progress'
_AA='Resource does not exist.'
_A9='Requested resource does not exist.'
_A8='2019-04-30'
_A7='urn:ietf:params:xml:ns:yang:ietf-yang-types'
_A6='ietf-yang-types'
_A5='module-set-id'
_A4='ietf-yang-library:modules-state'
_A3='application/yang-data+xml'
_A2='webhooks'
_A1='callout-type'
_A0='passed-input'
_z='ssl_object'
_y='access-denied'
_x='bad-attribute'
_w='/ietf-sztp-bootstrap-server:get-bootstrapping-data'
_v='Parent node does not exist.'
_u='Resource can not be modified.'
_t='/sztpd:devices/device='
_s='2024-10-10'
_r='2013-07-15'
_q='webhook'
_p='exited-normally'
_o='operation-not-supported'
_n='opaque'
_m='plugin'
_l='rpc-supported'
_k='data-missing'
_j='Unable to parse "input" document: '
_i='sztpd:device'
_h='import'
_g='Content-Type'
_f=False
_e='application/yang-data+json'
_d='function'
_c='call-function'
_b='malformed-message'
_a='implement'
_Z='function-results'
_Y='application'
_X='unknown-element'
_W='invalid-value'
_V=True
_U='path'
_T='method'
_S='source-ip'
_R='timestamp'
_Q='conformance-type'
_P='namespace'
_O='revision'
_N='error-tag'
_M='ietf-sztp-bootstrap-server:input'
_L='yangcore:dynamic-callout'
_K='error'
_J='protocol'
_I='text/plain'
_H='ietf-restconf:errors'
_G='+'
_F='name'
_E='return-code'
_D='error-returned'
_C=None
_B='/'
_A='event-details'
import importlib.resources as importlib_resources,urllib.parse,datetime,asyncio,base64,json,os,aiohttp,yangson,basicauth
from aiohttp import web
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from passlib.hash import sha256_crypt
from pyasn1.type import univ
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1_modules import rfc5652
from yangcore import utils
from yangcore.native import Read
from yangcore.dal import NodeNotFound
from yangcore.rcsvr import RestconfServer
from yangcore.handler import RouteHandler
from yangcore.yl import yl_8525_to_7895
from sztpd.yl import sztpd_rfc8572_yang_library
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43);supported_media_types=_e,_A3;yl4errors={_A4:{_A5:'TBD','module':[{_F:_A6,_O:_r,_P:_A7,_Q:_h},{_F:'ietf-restconf',_O:'2017-01-26',_P:'urn:ietf:params:xml:ns:yang:ietf-restconf',_Q:_a},{_F:'ietf-netconf-acm',_O:'2018-02-14',_P:'urn:ietf:params:xml:ns:yang:ietf-netconf-acm',_Q:_h},{_F:'ietf-sztp-bootstrap-server',_O:_A8,_P:'urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server',_Q:_a},{_F:'ietf-yang-structure-ext',_O:'2020-06-17',_P:'urn:ietf:params:xml:ns:yang:ietf-yang-structure-ext',_Q:_a},{_F:'ietf-ztp-types',_O:_s,_P:'urn:ietf:params:xml:ns:yang:ietf-ztp-types',_Q:_a},{_F:'ietf-sztp-csr',_O:_s,_P:'urn:ietf:params:xml:ns:yang:ietf-sztp-csr',_Q:_a},{_F:'ietf-crypto-types',_O:_s,_P:'urn:ietf:params:xml:ns:yang:ietf-crypto-types',_Q:_a}]}};yl4conveyedinfo={_A4:{_A5:'TBD','module':[{_F:_A6,_O:_r,_P:_A7,_Q:_h},{_F:'ietf-inet-types',_O:_r,_P:'urn:ietf:params:xml:ns:yang:ietf-inet-types',_Q:_h},{_F:'ietf-sztp-conveyed-info',_O:_A8,_P:'urn:ietf:params:xml:ns:yang:ietf-sztp-conveyed-info',_Q:_a}]}}
	def __init__(A,dal,yl_obj,nvh):E='sztpd';D='yang';A.dal=dal;A.nvh=nvh;B=importlib_resources.files('yangcore')/D;C=importlib_resources.files(E)/D;F=yl_8525_to_7895(yl_obj);A.dm=yangson.DataModel(json.dumps(F),[B,C]);A.dm4conveyedinfo=yangson.DataModel(json.dumps(A.yl4conveyedinfo),[B,C]);G=importlib_resources.files(E)/'yang4errors';A.dm4errors=yangson.DataModel(json.dumps(A.yl4errors),[G,B,C])
	async def _insert_bootstrapping_log_record(A,device_id,bootstrapping_log_record):B=_t+device_id[0]+'/bootstrapping-log';C={'sztpd:bootstrapping-log-record':bootstrapping_log_record};await A.dal.handle_post_opstate_request(B,C)
	async def handle_get_restconf_root(D,request):
		C=request;J=_B;F=await D._check_auth(C,J)
		if isinstance(F,web.Response):A=F;return A
		H=F;B={};B[_R]=datetime.datetime.utcnow();B[_S]=C.remote;B[_T]=C.method;B[_U]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_V)
		if isinstance(E,web.Response):A=E;L=K;B[_E]=A.status;B[_D]=L;await D._insert_bootstrapping_log_record(H,B);return A
		assert isinstance(E,str);G=E;assert G!=_I;I=utils.Encoding[G.rsplit(_G,1)[1].upper()];A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.JSON:A.text='{\n    "ietf-restconf:restconf" : {\n        "data" : {},\n        "operations" : {},\n        "yang-library-version" : "2019-01-04"\n    }\n}\n'
		else:assert I==utils.Encoding.XML;A.text='<restconf xmlns="urn:ietf:params:xml:ns:yang:ietf-restconf">\n    <data/>\n    <operations/>\n    <yang-library-version>2016-06-21</yang-library-version>\n</restconf>\n'
		B[_E]=A.status;await D._insert_bootstrapping_log_record(H,B);return A
	async def handle_get_yang_library_version(D,request):
		C=request;J=_B;F=await D._check_auth(C,J)
		if isinstance(F,web.Response):A=F;return A
		H=F;B={};B[_R]=datetime.datetime.utcnow();B[_S]=C.remote;B[_T]=C.method;B[_U]=C.path;E,K=utils.check_http_headers(C,D.supported_media_types,accept_required=_V)
		if isinstance(E,web.Response):A=E;L=K;B[_E]=A.status;B[_D]=L;await D._insert_bootstrapping_log_record(H,B);return A
		assert isinstance(E,str);G=E;assert G!=_I;I=utils.Encoding[G.rsplit(_G,1)[1].upper()];A=web.Response(status=200);A.content_type=G
		if I==utils.Encoding.JSON:A.text='{\n  "ietf-restconf:yang-library-version" : "2019-01-04"\n}'
		else:assert I==utils.Encoding.XML;A.text='<yang-library-version xmlns="urn:ietf:params:xml:ns:'+'yang:ietf-restconf">2019-01-04</yang-library-version>'
		B[_E]=A.status;await D._insert_bootstrapping_log_record(H,B);return A
	async def handle_get_opstate_request(C,request):
		D=request;F=D.path[C.len_prefix_operational:];F=_B;G=await C._check_auth(D,F)
		if isinstance(G,web.Response):A=G;return A
		I=G;B={};B[_R]=datetime.datetime.utcnow();B[_S]=D.remote;B[_T]=D.method;B[_U]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_V)
		if isinstance(E,web.Response):A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_record(I,B);return A
		assert isinstance(E,str);H=E;assert H!=_I;J=utils.Encoding[H.rsplit(_G,1)[1].upper()]
		if F in('',_B,'/ietf-yang-library:yang-library'):A=web.Response(status=200);A.content_type=_e;A.text=json.dumps(sztpd_rfc8572_yang_library())
		else:A=web.Response(status=404);A.content_type=H;J=utils.Encoding[A.content_type.rsplit(_G,1)[1].upper()];K=utils.gen_rc_errors(_J,_X,error_message=_A9);N=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_E]=A.status;await C._insert_bootstrapping_log_record(I,B);return A
	async def handle_get_config_request(C,request):
		D=request;H=D.path[C.len_prefix_running:];F=await C._check_auth(D,H)
		if isinstance(F,web.Response):A=F;return A
		I=F;B={};B[_R]=datetime.datetime.utcnow();B[_S]=D.remote;B[_T]=D.method;B[_U]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_V)
		if isinstance(E,web.Response):A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_record(I,B);return A
		assert isinstance(E,str);G=E;assert G!=_I;J=utils.Encoding[G.rsplit(_G,1)[1].upper()]
		if H in('',_B):A=web.Response(status=204)
		else:A=web.Response(status=404);A.content_type=G;J=utils.Encoding[A.content_type.rsplit(_G,1)[1].upper()];K=utils.gen_rc_errors(_J,_X,error_message=_A9);N=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(K,J,C.dm4errors,N);B[_D]=K
		B[_E]=A.status;await C._insert_bootstrapping_log_record(I,B);return A
	async def handle_post_config_request(C,request):
		D=request;I=D.path[C.len_prefix_running:];F=await C._check_auth(D,I)
		if isinstance(F,web.Response):A=F;return A
		J=F;B={};B[_R]=datetime.datetime.utcnow();B[_S]=D.remote;B[_T]=D.method;B[_U]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if isinstance(E,web.Response):A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_record(J,B);return A
		assert isinstance(E,str);G=E;assert G!=_I;K=utils.Encoding[G.rsplit(_G,1)[1].upper()]
		if I in('',_B):A=web.Response(status=400);H=utils.gen_rc_errors(_Y,_W,error_message=_u)
		else:A=web.Response(status=404);H=utils.gen_rc_errors(_J,_X,error_message=_v)
		A.content_type=G;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]].upper();N=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(H,K,C.dm4errors,N);B[_E]=A.status;B[_D]=H;await C._insert_bootstrapping_log_record(J,B);return A
	async def handle_put_config_request(C,request):
		D=request;I=D.path[C.len_prefix_running:];F=await C._check_auth(D,I)
		if isinstance(F,web.Response):A=F;return A
		J=F;B={};B[_R]=datetime.datetime.utcnow();B[_S]=D.remote;B[_T]=D.method;B[_U]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if isinstance(E,web.Response):A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_record(J,B);return A
		assert isinstance(E,str);G=E;assert G!=_I;K=utils.Encoding[G.rsplit(_G,1)[1].upper()]
		if I in('',_B):A=web.Response(status=400);H=utils.gen_rc_errors(_Y,_W,error_message=_u)
		else:A=web.Response(status=404);H=utils.gen_rc_errors(_J,_X,error_message=_v)
		A.content_type=G;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]].upper();N=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(H,K,C.dm4errors,N);B[_E]=A.status;B[_D]=H;await C._insert_bootstrapping_log_record(J,B);return A
	async def handle_delete_config_request(C,request):
		D=request;K=D.path[C.len_prefix_running:];G=await C._check_auth(D,K)
		if isinstance(G,web.Response):A=G;return A
		L=G;B={};B[_R]=datetime.datetime.utcnow();B[_S]=D.remote;B[_T]=D.method;B[_U]=D.path;E,M=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if isinstance(E,web.Response):A=E;N=M;B[_E]=A.status;B[_D]=N;await C._insert_bootstrapping_log_record(L,B);return A
		assert isinstance(E,str);H=E
		if H==_I:I=_C
		else:I=utils.Encoding[H.rsplit(_G,1)[1].upper()]
		if K in('',_B):A=web.Response(status=400);F=_u;J=utils.gen_rc_errors(_Y,_W,error_message=F)
		else:A=web.Response(status=404);F=_v;J=utils.gen_rc_errors(_J,_X,error_message=F)
		A.content_type=H
		if I is _C:A.text=F
		else:O=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(J,I,C.dm4errors,O)
		B[_E]=A.status;B[_D]=J;await C._insert_bootstrapping_log_record(L,B);return A
	async def handle_action_request(C,request):
		D=request;I=D.path[C.len_prefix_operational:];F=await C._check_auth(D,I)
		if isinstance(F,web.Response):A=F;return A
		J=F;B={};B[_R]=datetime.datetime.utcnow();B[_S]=D.remote;B[_T]=D.method;B[_U]=D.path;E,L=utils.check_http_headers(D,C.supported_media_types,accept_required=_f)
		if isinstance(E,web.Response):A=E;M=L;B[_E]=A.status;B[_D]=M;await C._insert_bootstrapping_log_record(J,B);return A
		assert isinstance(E,str);G=E;assert G!=_I;K=utils.Encoding[G.rsplit(_G,1)[1].upper()]
		if I in('',_B):A=web.Response(status=400);H=utils.gen_rc_errors(_Y,_W,error_message='Resource does not support action.')
		else:A=web.Response(status=404);H=utils.gen_rc_errors(_J,_X,error_message=_AA)
		A.content_type=G;K=utils.Encoding[A.content_type.rsplit(_G,1)[1]].upper();N=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(H,K,C.dm4errors,N);B[_E]=A.status;B[_D]=H;await C._insert_bootstrapping_log_record(J,B);return A
	async def handle_rpc_request(D,request):
		J='sleep';B=request;F=B.path[D.len_prefix_operations:];G=await D._check_auth(B,F)
		if isinstance(G,web.Response):C=G;return C
		E=G;A={};A[_R]=datetime.datetime.utcnow();A[_S]=B.remote;A[_T]=B.method;A[_U]=B.path
		if F==_w:
			async with D.nvh.fifolock(Read):
				if os.environ.get('SZTPD_INIT_MODE')and J in B.query:await asyncio.sleep(int(B.query[J]))
				C=await D._handle_get_bootstrapping_data_rpc(E,B,A);A[_E]=C.status;await D._insert_bootstrapping_log_record(E,A)
			return C
		if F==_AB:C=await D._handle_report_progress_rpc(E,B,A);A[_E]=C.status;await D._insert_bootstrapping_log_record(E,A);return C
		if F in(''or _B):C=web.Response(status=400);H=_AA
		else:C=web.Response(status=404);H='Unrecognized RPC.'
		I,K=utils.format_resp_and_msg(C,H,_x,B,D.supported_media_types);A[_E]=I.status;A[_D]=K;await D._insert_bootstrapping_log_record(E,A);return I
	async def _check_auth(A,request,data_path):
		i='num-times-accessed';h='central-truststore-reference';g='sztpd:device-type';f='identity-certificates';e='activation-code';d='X-Client-Cert';T='verification';S='device-type';O='sbi-access-stats';K='lifecycle-statistics';I='comment';H='failure';E='outcome';C=request;assert data_path[0]==_B
		def F(request,supported_media_types):
			E=supported_media_types;D='Accept';C=request;B=web.Response(status=401)
			if D in C.headers and any(C.headers[D]==A for A in E):B.content_type=C.headers[D]
			elif _g in C.headers and any(C.headers[_g]==A for A in E):B.content_type=C.headers[_g]
			else:B.content_type=_I
			if B.content_type!=_I:F=utils.Encoding[B.content_type.rsplit(_G,1)[1].upper()];G=utils.gen_rc_errors(_J,_y);H=A.dm4errors.get_schema_node(_B);B.text=utils.obj_to_encoded_str(G,F,A.dm4errors,H)
			return B
		B={};B[_R]=datetime.datetime.utcnow();B[_S]=C.remote;B['source-proxies']=list(C.forwarded);B['host']=C.host;B[_T]=C.method;B[_U]=C.path;J=set();L=_C;M=C.transport.get_extra_info('peercert')
		if M is not _C:N=M['subject'][-1][0][1];J.add(N)
		elif C.headers.get(d)is not _C:j=C.headers.get(d);U=bytes(urllib.parse.unquote(j),'utf-8');L=x509.load_pem_x509_certificate(U,default_backend());k=L.subject;N=k.get_attributes_for_oid(x509.ObjectIdentifier('2.5.4.5'))[0].value;J.add(N)
		P=_C;V=_C;Q=C.headers.get('AUTHORIZATION')
		if Q is not _C:P,V=basicauth.decode(Q);J.add(P)
		if len(J)==0:B[E]=H;B[I]='Device provided no identification credentials.';await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
		if len(J)!=1:B[E]=H;B[I]='Device provided mismatched authentication credentials ('+N+' != '+P+').';await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
		G=J.pop();D=_C;W=_t+G
		try:D=await A.dal.handle_get_opstate_request(W,{})
		except NodeNotFound:B[E]=H;B[I]='Device "'+G+'" not found for any tenant.';await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
		l=_C;assert D is not _C;assert _i in D;D=D[_i][0]
		if e in D:
			if Q is _C:B[E]=H;B[I]='Activation code required but none passed for serial number '+G;await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
			X=D[e];assert X.startswith('$5$')
			if not sha256_crypt.verify(V,X):B[E]=H;B[I]='Activation code mismatch for serial number '+G;await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
		assert S in D;m='/sztpd:device-types/device-type='+D[S];Y=await A.dal.handle_get_opstate_request(m,{})
		if f in Y[g][0]:
			if M is _C and L is _C:B[E]=H;B[I]='Client cert required but none passed for serial number '+G;await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
			if M:Z=C.transport.get_extra_info(_z);assert Z is not _C;a=Z.getpeercert(_V)
			else:assert L is not _C;a=U
			R=Y[g][0][f];assert T in R;assert h in R[T];b=R[T][h];n='/ietf-truststore:truststore/certificate-bags/certificate-bag='+b['certificate-bag']+'/certificate='+b['certificate'];o=await A.dal.handle_get_config_request(n,{});p=o['ietf-truststore:certificate'][0]['cert-data'];q=base64.b64decode(p);r,s=der_decoder(q,asn1Spec=rfc5652.ContentInfo());assert not s;t=utils.degenerate_cms_obj_to_ders(r);u=ValidationContext(trust_roots=t);v=CertificateValidator(a,validation_context=u)
			try:v._validate_path()
			except PathBuildingError:B[E]=H;B[I]="Client cert for serial number '"+G+"' does not validate using trust anchors specified by device-type '"+D[S]+"'";await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);return F(C,A.supported_media_types)
		B[E]='success';await utils.insert_audit_log_record(A.dal,A.nvh.plugins,B);w=W+'/lifecycle-statistics';c=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		if D[K][O][i]==0:D[K][O]['first-accessed']=c
		D[K][O]['last-accessed']=c;D[K][O][i]+=1;await A.dal.handle_put_opstate_request(w,D[K]);return G,l
	async def _handle_get_bootstrapping_data_rpc(B,device_id,request,bootstrapping_log_record):
		AR='ietf-sztp-bootstrap-server:output';AQ='content';AP='contentType';AO='sztpd:configuration';AN='sztpd:script';AM='/sztpd:conveyed-information/scripts/script=';AL='hash-value';AK='hash-algorithm';AJ='os-version';AI='os-name';AH='address';AG='referenced-definition';AF='match-criteria';AE='matched-response';A5=device_id;A4='post-configuration-script';A3='configuration';A2='pre-configuration-script';A1='trust-anchor';A0='port';z='bootstrap-server';y='ietf-sztp-conveyed-info:redirect-information';x='value';w='response-manager';o='image-verification';n='download-uri';m='boot-image';l='via-onboarding-response';k='via-redirect-response';j='reference';i='selected-response';e='key';X=request;W='ietf-sztp-conveyed-info:onboarding-information';Q='response';N='via-dynamic-callout';J='managed-response';I='response-details';E='get-bootstrapping-data-event';D='conveyed-information';C=bootstrapping_log_record;f,AS=utils.check_http_headers(X,B.supported_media_types,accept_required=_V)
		if isinstance(f,web.Response):A=f;AT=AS;C[_E]=A.status;C[_D]=AT;return A
		assert isinstance(f,str);O=f;assert O!=_I;R=utils.Encoding[O.rsplit(_G,1)[1].upper()];K=_C
		if X.body_exists:
			AU=await X.text();AV=utils.Encoding[X.headers[_g].rsplit(_G,1)[1].upper()];F=B.dm.get_schema_node(_w)
			try:K=utils.encoded_str_to_obj(AU,AV,B.dm,F)
			except utils.TranscodingError as Y:A=web.Response(status=400);p=_j+str(Y);A.content_type=O;G=utils.gen_rc_errors(_J,_b,error_message=p);F=B.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(G,R,B.dm4errors,F);C[_D]=G;return A
			if not _M in K:
				A=web.Response(status=400)
				if not _M in K:p=_j+_AC
				A.content_type=O;G=utils.gen_rc_errors(_J,_b,error_message=p);F=B.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(G,R,B.dm4errors,F);C[_D]=G;return A
		C[_A]={};C[_A][E]={}
		if K is _C:C[_A][E][_A0]={'no-input-passed':[_C]}
		else:C[_A][E][_A0]=K[_M]
		A6=_C
		if K:
			try:A6=K[_M]
			except KeyError:A=web.Response(status=400);A.content_type=_e;G=utils.gen_rc_errors(_J,_W,error_message='RPC "input" node missing.');A.text=utils.enc_rc_errors('json',G);return A
			F=B.dm.get_schema_node('/ietf-sztp-bootstrap-server:get-bootstrapping-data/input')
			try:F.from_raw(A6)
			except yangson.exceptions.RawMemberError as Y:A=web.Response(status=400);A.content_type=_e;G=utils.gen_rc_errors(_J,_W,error_message='RPC "input" node fails YANG validation here: '+str(Y));A.text=utils.enc_rc_errors('json',G);return A
		AW=_t+A5[0];T=await B.dal.handle_get_config_request(AW,{});assert T is not _C;assert _i in T;T=T[_i][0]
		if w not in T or AE not in T[w]:A=web.Response(status=404);A.content_type=O;G=utils.gen_rc_errors(_Y,_k,error_message='No responses configured.');F=B.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(G,R,B.dm4errors,F);C[_D]=G;C[_A][E][i]='no-responses-configured';return A
		H=_C
		for g in T[w][AE]:
			if not AF in g:H=g;break
			if K is _C:continue
			for P in g[AF]['match']:
				if P[e]not in K[_M]:break
				if'present'in P:
					if'not'in P:
						if P[e]in K[_M]:break
					elif P[e]not in K[_M]:break
				elif x in P:
					if'not'in P:
						if P[x]==K[_M][P[e]]:break
					elif P[x]!=K[_M][P[e]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:H=g;break
		if H is _C or'none'in H[Q]:
			if H is _C:C[_A][E][i]='no-match-found'
			else:C[_A][E][i]=H[_F]+" (explicit 'none')"
			A=web.Response(status=404);A.content_type=O;G=utils.gen_rc_errors(_Y,_k,error_message='No matching responses configured.');F=B.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(G,R,B.dm4errors,F);C[_D]=G;return A
		C[_A][E][i]=H[_F];C[_A][E][I]={J:{}}
		if D in H[Q]:
			C[_A][E][I][J]={D:{}};M={}
			if N in H[Q][D]:
				C[_A][E][I][J][D]={N:{}};assert j in H[Q][D][N];q=H[Q][D][N][j];C[_A][E][I][J][D][N][_F]=q;r=await B.dal.handle_get_config_request(_AD+q,{});U=r[_L][0];assert q==U[_F];C[_A][E][I][J][D][N][_l]=U[_l];b={};b[_AE]=A5[0];b[_AF]=X.remote;A7=X.transport.get_extra_info(_z)
				if A7:
					A8=A7.getpeercert(_V)
					if A8:b[_AG]=A8
				if K:b[_AH]=K
				if _c in U:
					C[_A][E][I][J][D][N][_A1]=_d;A9=U[_c][_m];AA=U[_c][_d];C[_A][E][I][J][D][N][_AI]={_m:A9,_d:AA};C[_A][E][I][J][D][N][_Z]={}
					if _n in U:AB=U[_n]
					else:AB=_C
					L=_C
					try:L=B.nvh.plugins[A9][_AJ][AA](b,AB)
					except Exception as Y:C[_A][E][I][J][D][N][_Z][_AK]=str(Y);A=web.Response(status=500);A.content_type=O;G=utils.gen_rc_errors(_Y,_o,error_message='Server '+'encountered an error while trying to generate '+'a response: '+str(Y));F=B.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(G,R,B.dm4errors,F);C[_D]=G;return A
					assert L and isinstance(L,dict)
					if _H in L:
						assert len(L[_H][_K])==1
						if any(A==L[_H][_K][0][_N]for A in(_W,'too-big',_AL,_x,_AM,_AN,_X,_AO,_b)):A=web.Response(status=400)
						elif any(A==L[_H][_K][0][_N]for A in _y):A=web.Response(status=403)
						elif any(A==L[_H][_K][0][_N]for A in('in-use',_AP,_AQ,_AR,_k)):A=web.Response(status=409)
						elif any(A==L[_H][_K][0][_N]for A in(_AS,_AT,_AU)):A=web.Response(status=500)
						elif any(A==L[_H][_K][0][_N]for A in _o):A=web.Response(status=501)
						else:raise NotImplementedError(_AV+L[_H][_K][0][_N])
						A.content_type=O;G=L;F=B.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(G,R,B.dm4errors,F);C[_D]=L;C[_A][E][I][J][D][N][_Z][_p]='Returning an RPC-error provided by function (NOTE: RPC-error '+'!= exception, hence a normal exit).';return A
					C[_A][E][I][J][D][N][_Z][_p]='Returning conveyed information provided by function.'
				elif _A2 in r[_L][0]:C[_A][E][I][J][D][N][_A1]=_q;raise NotImplementedError('webhooks were disabled!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(r[_L][0]))
				M=L[D]
			elif k in H[Q][D]:
				C[_A][E][I][J][D]={k:{}};M[y]={};M[y][z]=[];c=H[Q][D][k][j];C[_A][E][I][J][D][k]={AG:c};s=await B.dal.handle_get_config_request('/sztpd:responses/redirect-response='+c,{})
				for AX in s['sztpd:redirect-response'][0]['redirect-information'][z]:
					V=await B.dal.handle_get_config_request('/sztpd:conveyed-information/bootstrap-servers/bootstrap-server='+AX,{});V=V['sztpd:bootstrap-server'][0];h={};h[AH]=V[AH]
					if A0 in V:h[A0]=V[A0]
					if A1 in V:h[A1]=V[A1]
					M[y][z].append(h)
			elif l in H[Q][D]:
				C[_A][E][I][J][D]={l:{}};M[W]={};c=H[Q][D][l][j];C[_A][E][I][J][D][l]={AG:c};s=await B.dal.handle_get_config_request('/sztpd:responses/onboarding-response='+c,{});S=s['sztpd:onboarding-response'][0]['onboarding-information']
				if m in S:
					AY=S[m];AZ=await B.dal.handle_get_config_request('/sztpd:conveyed-information/boot-images/boot-image='+AY,{});Z=AZ['sztpd:boot-image'][0];M[W][m]={};a=M[W][m];a[AI]=Z[AI];a[AJ]=Z[AJ]
					if n in Z:
						a[n]=[]
						for Aa in Z[n]:a[n].append(Aa)
					if o in Z:
						a[o]=[]
						for AC in Z[o]:t={};t[AK]=AC[AK];t[AL]=AC[AL];a[o].append(t)
				if A2 in S:Ab=S[A2];Ac=await B.dal.handle_get_config_request(AM+Ab,{});M[W][A2]=Ac[AN][0]['code']
				if A3 in S:Ad=S[A3];AD=await B.dal.handle_get_config_request('/sztpd:conveyed-information/configurations/configuration='+Ad,{});M[W]['configuration-handling']=AD[AO][0]['handling'];M[W][A3]=AD[AO][0]['config-data']
				if A4 in S:Ae=S[A4];Af=await B.dal.handle_get_config_request(AM+Ae,{});M[W][A4]=Af[AN][0]['code']
		else:raise NotImplementedError('unhandled response type: '+str(H[Q]))
		d=rfc5652.ContentInfo()
		if O==_e:d[AP]=B.id_ct_sztpConveyedInfoJSON;d[AQ]=encode_der(json.dumps(M,indent=2),asn1Spec=univ.OctetString())
		else:assert O==_A3;d[AP]=B.id_ct_sztpConveyedInfoXML;F=B.dm4conveyedinfo.get_schema_node(_B);assert F;Ag=utils.obj_to_encoded_str(M,R,B.dm4conveyedinfo,F,strip_wrapper=_V);d[AQ]=encode_der(Ag,asn1Spec=univ.OctetString())
		Ah=encode_der(d,rfc5652.ContentInfo());u=base64.b64encode(Ah).decode('ASCII');Ai=base64.b64decode(u);Aj=base64.b64encode(Ai).decode('ASCII');assert u==Aj;v={};v[AR]={};v[AR][D]=u;A=web.Response(status=200);A.content_type=O;F=B.dm.get_schema_node(_w);A.text=utils.obj_to_encoded_str(v,R,B.dm,F);return A
	async def _handle_report_progress_rpc(C,device_id,request,bootstrapping_log_record):
		f='remote-port';e='webhook-results';d='sztpd:relay-progress-report-callout';X='tcp-client-parameters';U='http';K=request;G='dynamic-callout';E='report-progress-event';B=bootstrapping_log_record;S,g=utils.check_http_headers(K,C.supported_media_types,accept_required=_f)
		if isinstance(S,web.Response):A=S;h=g;B[_E]=A.status;B[_D]=h;return A
		assert isinstance(S,str);J=S
		if J==_I:L=_I
		else:i=J.rsplit(_G,1)[1].upper();L=utils.Encoding[i]
		if not K.body_exists:
			M='RPC "input" node missing (required for "report-progress").';A=web.Response(status=400);A.content_type=J
			if A.content_type==_I:A.text=M
			else:F=utils.gen_rc_errors(_J,_W,error_message=M);H=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(F,L,C.dm4errors,H)
			B[_D]=A.text;return A
		j=utils.Encoding[K.headers[_g].rsplit(_G,1)[1].upper()];k=await K.text();H=C.dm.get_schema_node(_AB)
		try:Q=utils.encoded_str_to_obj(k,j,C.dm,H)
		except utils.TranscodingError as N:A=web.Response(status=400);M=_j+str(N);A.content_type=J;F=utils.gen_rc_errors(_J,_b,error_message=M);H=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(F,L,C.dm4errors,H);B[_D]=F;return A
		if not _M in Q:
			A=web.Response(status=400)
			if not _M in Q:M=_j+_AC
			A.content_type=J;F=utils.gen_rc_errors(_J,_b,error_message=M);H=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(F,L,C.dm4errors,H);B[_D]=F;return A
		B[_A]={};B[_A][E]={};B[_A][E][_A0]=Q[_M];B[_A][E][G]={};V='/yangcore:preferences/outbound-interactions/'+d
		try:l=await C.dal.handle_get_config_request(V,{})
		except NodeNotFound:B[_A][E][G]['no-callout-configured']=[_C];A=web.Response(status=204);return A
		W=l[d];B[_A][E][G][_F]=W;V=_AD+W;I=await C.dal.handle_get_config_request(V,{});assert W==I[_L][0][_F];B[_A][E][G][_l]=I[_L][0][_l];O={};O[_AE]=device_id[0];O[_AF]=K.remote;Y=K.transport.get_extra_info(_z)
		if Y:
			Z=Y.getpeercert(_V)
			if Z:O[_AG]=Z
		if Q:O[_AH]=Q
		if _c in I[_L][0]:
			B[_A][E][G][_A1]=_d;a=I[_L][0][_c][_m];b=I[_L][0][_c][_d];B[_A][E][G][_AI]={_m:a,_d:b};B[_A][E][G][_Z]={}
			if _n in I[_L][0]:c=I[_L][0][_n]
			else:c=_C
			D=_C
			try:D=C.nvh.plugins[a][_AJ][b](O,c)
			except Exception as N:B[_A][E][G][_Z][_AK]=str(N);A=web.Response(status=500);A.content_type=J;F=utils.gen_rc_errors(_Y,_o,error_message='Server encountered an error while trying '+'to process the progress report: '+str(N));H=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(F,L,C.dm4errors,H);B[_D]=F;return A
			if D:
				assert isinstance(D,dict);assert len(D)==1;assert _H in D;assert len(D[_H][_K])==1
				if any(A==D[_H][_K][0][_N]for A in(_W,'too-big',_AL,_x,_AM,_AN,_X,_AO,_b)):A=web.Response(status=400)
				elif any(A==D[_H][_K][0][_N]for A in _y):A=web.Response(status=403)
				elif any(A==D[_H][_K][0][_N]for A in('in-use',_AP,_AQ,_AR,_k)):A=web.Response(status=409)
				elif any(A==D[_H][_K][0][_N]for A in(_AS,_AT,_AU)):A=web.Response(status=500)
				elif any(A==D[_H][_K][0][_N]for A in _o):A=web.Response(status=501)
				else:raise NotImplementedError(_AV+D[_H][_K][0][_N])
				A.content_type=J;F=D;H=C.dm4errors.get_schema_node(_B);A.text=utils.obj_to_encoded_str(F,L,C.dm4errors,H);B[_D]=D;B[_A][E][G][_Z][_p]='Returning an RPC-error provided by function '+'(NOTE: RPC-error != exception, hence a normal exit).';return A
			B[_A][E][G][_Z][_p]='Function returned no output (normal)'
		elif _A2 in I[_L][0]:
			B[_A][E][G][e]={_q:[]}
			for P in I[_L][0][_A2][_q]:
				R={};R[_F]=P[_F]
				if U in P:
					T='http://'+P[U][X]['remote-address']
					if f in P[U][X]:T+=':'+str(P[U][X][f])
					T+='/relay-notification';R['uri']=T
					try:
						async with aiohttp.ClientSession()as m:A=await m.post(T,data=O)
					except aiohttp.client_exceptions.ClientConnectorError as N:R['connection-error']=str(N)
					else:
						R['http-status-code']=A.status
						if A.status==200:break
				else:assert'https'in P;raise NotImplementedError('https-based webhook is not supported yet.')
				B[_A][E][G][e][_q].append(R)
		else:raise NotImplementedError('unrecognized callout type '+str(I[_L][0]))
		A=web.Response(status=204);return A# Copyright (c) 2020-2025 Watsen Networks. All Rights Reserved.

