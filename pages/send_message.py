import streamlit as st
import os
from dotenv import load_dotenv
from classifier import classify_message

load_dotenv()

st.title("📝 Kirim Pesan")

with st.form("message_form"):
    message = st.text_area(
        "Tulis pesan Anda (dalam Bahasa Indonesia):",
        placeholder="Contoh: Lampu di toilet mati dan pelayan tidak menanggapi...",
        height=150
    )
    
    submitted = st.form_submit_button("Kirim Pesan")
    
    if submitted and message.strip():
        with st.spinner("Mengklasifikasi pesan..."):
            try:
                result = classify_message(message.strip())
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    try:
                        import json
                        import requests
                        
                        supabase_url = os.getenv('SUPABASE_URL')
                        supabase_key = os.getenv('SUPABASE_KEY')
                        
                        if not supabase_url or not supabase_key:
                            raise Exception("Supabase credentials not found in environment variables")
                        
                        headers = {
                            'apikey': supabase_key,
                            'Authorization': f'Bearer {supabase_key}',
                            'Content-Type': 'application/json'
                        }
                        
                        urgency_order = 1 if result['urgency'] == 'Extremely Urgent' else 2 if result['urgency'] == 'Urgent' else 3
                        
                        data = {
                            'message_text': message,
                            'urgency': result['urgency'],
                            'groups': result['groups'],
                            'action_message': result.get('action_message', ''),
                            'urgency_order': urgency_order
                        }
                        
                        response = requests.post(
                            f"{supabase_url}/rest/v1/messages",
                            headers=headers,
                            json=data
                        )
                        
                        if response.status_code not in [200, 201]:
                            raise Exception(f"Supabase error: {response.text}")
                        
                        st.success("✅ Pesan berhasil dikirim dan diklasifikasi!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"**Tingkat Urgensi:** {result['urgency']}")
                        with col2:
                            st.info(f"**Kategori:** {', '.join(result['groups'])}")
                            
                    except Exception as db_error:
                        st.error(f"Error menyimpan ke database: {db_error}")
                        st.json(result)
                        
            except Exception as e:
                st.error(f"Error mengklasifikasi pesan: {e}")
    
    elif submitted:
        st.warning("Mohon masukkan pesan terlebih dahulu.")
