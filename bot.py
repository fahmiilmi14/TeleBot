import os
import requests
from groq import Groq
from tavily import TavilyClient
from datetime import date

hari_ini = date.today()

def get_market_analysis():
    try:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        query = f"harga emas antam hari ini, poin IHSG terbaru, dan analisis ekonomi Indonesia terkini tanggal {hari_ini}"
        search_result = tavily.search(query=query, search_depth="advanced")

        prompt = f"""
        Kamu adalah asisten analis keuangan profesional. Berdasarkan data berikut:
        {search_result}
        
        Berikan laporan singkat untuk Telegram dengan format Markdown:
        💰 **KONDISI SAAT INI**
        - Harga Emas Antam: [Sebutkan harga]
        - Poin IHSG: [Sebutkan poin]
        
        📈 **PREDIKSI & SENTIMEN**
        [Berikan analisis singkat tren ke depan berdasarkan berita]
        
        🚦 **REKOMENDASI**
        **[BELI / TUNGGU / JUAL]**
        Alasan: [Berikan alasan logis dari kacamata ekonomi]
        
        ⚠️ *Disclaimer: Ini adalah analisis AI, bukan saran keuangan mutlak.*
        """
        
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        report = completion.choices[0].message.content

        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": f"🔔 **IKI INTEL UPDATE**\n\n{report}",
            "parse_mode": "Markdown"
        }
        
        requests.post(url, json=payload)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_market_analysis()
