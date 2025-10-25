import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("📊 Dashboard")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    urgency_filter = st.selectbox(
        "Filter by Urgency:",
        ["All", "Not Urgent", "Urgent", "Extremely Urgent"]
    )

with col2:
    group_filter = st.selectbox(
        "Filter by Group:",
        ["All", "Facility", "The Waiters", "The Chef", "Cleanse", "Administration", "Hospitality", "The Foods"]
    )

with col3:
    search_term = st.text_input("Search messages:", placeholder="Ketik kata kunci...")

if st.button("🔄 Refresh Data"):
    st.rerun()

try:
    import requests
    import json
    
    # Use Supabase REST API
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        st.error("Supabase credentials not found in environment variables")
        st.stop()
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    # Build query parameters
    params = {'select': '*', 'order': 'urgency_order.asc,created_at.desc'}
    
    if urgency_filter != "All":
        params['urgency'] = f'eq.{urgency_filter}'
    
    if group_filter != "All":
        params['groups'] = f'cs.{{"{group_filter}"}}'
    
    if search_term:
        params['message_text'] = f'ilike.*{search_term}*'
    
    response = requests.get(
        f"{supabase_url}/rest/v1/messages",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        
        if data:
            st.success(f"Menampilkan {len(data)} pesan")
            
            for row in data:
                # Trim message and remove newlines
                display_message = row['message_text'].replace('\n', ' ').strip()
                if len(display_message) > 500:
                    display_message = display_message[:500] + "..."
                
                # Set color based on urgency
                if row['urgency'] == 'Extremely Urgent':
                    color = "🔴"
                    bg_color = "#ffebee"
                elif row['urgency'] == 'Urgent':
                    color = "🟡"
                    bg_color = "#fff8e1"
                else:  # Not Urgent
                    color = "🟢"
                    bg_color = "#e8f5e8"
                
                with st.expander(f"{color} {display_message}", expanded=False):
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px;">
                    <strong>Pesan Lengkap:</strong><br>{row['message_text']}<br><br>
                    <strong>Urgensi:</strong> {row['urgency']}<br>
                    <strong>Kategori:</strong> {', '.join(row['groups']) if row['groups'] else 'None'}<br>
                    <strong>Waktu:</strong> {row['created_at']}<br>
                    <strong>ID:</strong> {row['id']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Belum ada pesan yang tersimpan.")
    else:
        st.error(f"Error mengambil data: {response.text}")
        
except Exception as e:
    st.error(f"Error mengambil data: {e}")
    st.info("Pastikan database sudah dibuat dan terhubung dengan benar.")
