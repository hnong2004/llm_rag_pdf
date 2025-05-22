#!/usr/bin/env python3

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv(".env")

# ดึงค่า GROQ_API_KEY จากตัวแปรสภาพ .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# สร้าง client สำหรับใช้งาน Groq API
client = Groq(api_key=GROQ_API_KEY)


def chatboot(question):

    # กำหนด system prompt สำหรับ LLM เพื่อให้วิเคราะห์ความสุกของเมล่อนจากคำบรรยาย
    system_prompt = """
        น่าน เป็นจังหวัดหนึ่งในประเทศไทย ตั้งอยู่ทางทิศตะวันออกสุดของภาคเหนือ เป็นที่ตั้งของเมืองที่สำคัญในอดีต เช่น เวียงวรนคร (เมืองพลัว) เวียงศีรษะเกษ (เมืองงั่ว) เวียงภูเพียงแช่แห้ง อีกทั้งยังเป็นแหล่งต้นน้ำของแม่น้ำน่าน
ประวัติศาสตร์ มีประวัติความเป็นมาที่เก่าแก่ยาวนาน มีชื่อเรียกในพงศาวดารว่า นันทบุรี เมืองน่านในอดีตเป็นนครรัฐเล็ก ๆ ก่อตัวขึ้นราวกลางพุทธศตวรรษที่ 18 บริเวณที่ราบลุ่มแม่น้ำน่านและแม่น้ำสาขาในหุบเขาทางตะวันออกของภาคเหนือ
        """

    # ส่งคำถามและ system prompt ไปยัง LLM เพื่อรับคำตอบ
    response = client.chat.completions.create(
        # เลือกใช้โมเดล        
        model="llama-3.1-8b-instant",
        messages=[
            # กำหนดระบบให้เข้าใจบทบาท
            {"role": "system", "content": system_prompt},
            # ส่งคำถามจากผู้ใช้
            {"role": "user", "content": question},
        ],
        temperature=0.2,  # Fine-tuning 
        max_tokens= 256,  # เช็ค max_token ระวัง exceed API Key (ไม่เกินเท่าไหร่ ขึ้นอยู่กับโมเดล)
    )

    return response.choices[0].message.content.strip()


def main():
    """แสดงและจัดการหน้าของแอป Streamlit"""

    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

    st.title(" ")
    st.subheader(" ")

    with st.form("chat_form"):
        query = st.text_input(" :", placeholder=" ...").strip()

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "  :)"}
            ]

        submitted = st.form_submit_button("Submit")

        if submitted and query:
            answer = chatboot(query)
            st.session_state["messages"].append({"role": "user", "content": query})
            st.session_state["messages"].append(
                {"role": "assistant", "content": answer}
            )
        elif submitted and not query:
            st.warning("Text before submiting")

    chat_area = st.empty()

    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            chat_area.write(f"**Bot:** {msg['content']}\n")
        else:
            chat_area.write(f"**You:** {msg['content']}\n")


if __name__ == "__main__":
    main()
