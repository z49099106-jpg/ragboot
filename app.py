import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="RAG Droit", page_icon="⚖️")
st.title("⚖️ مساعد كلية الحقوق - RAG")
st.markdown("حملي ملفات PDF واسألي أي سؤال من دروسك")

with st.sidebar:
    files = st.file_uploader("حملي PDF", type=["pdf"], accept_multiple_files=True)

def get_text(files):
    t=""
    for f in files:
        r=PdfReader(f)
        for p in r.pages:
            txt=p.extract_text()
            if txt:
                t+=txt+"\n"
    return t

if files:
    txt=get_text(files)
    chunks=[txt[i:i+1000] for i in range(0,len(txt),1000) if len(txt[i:i+1000].strip())>20]
    st.session_state['chunks']=chunks
    st.session_state['vect']=TfidfVectorizer().fit(chunks)
    st.session_state['vecs']=st.session_state['vect'].transform(chunks)
    st.sidebar.success(f"تم {len(chunks)} مقطع")

if 'chunks' in st.session_state:
    q=st.text_input("سؤالك:")
    if q:
        qv=st.session_state['vect'].transform([q])
        sims=cosine_similarity(qv, st.session_state['vecs'])[0]
        idx=sims.argsort()[-3:][::-1]
        for i in idx:
            if sims[i]>0.05:
                st.info(st.session_state['chunks'][i][:700])
