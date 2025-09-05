import streamlit as st
import json
import os
import random

# ---------- Yardımcı Fonksiyonlar ----------
def load_words():
    if os.path.exists("words.json"):
        with open("words.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "about to": "mak üzere",
        "abrupt": "ani",
        "absurd": "saçma",
        "abundant": "bol",
        "acceptable": "kabul edilebilir",
        "abnormal": "anormal",
        "accountable": "hesap verilebilir",
        "acquainted with": "tanıdık",
        "actual": "gerçek",
        "acute": "şiddetli derecede",
    }

def save_words(words):
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

def load_stats():
    if os.path.exists("stats.json"):
        with open("stats.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

# ---------- Uygulama Başlangıcı ----------
st.set_page_config(page_title="YDS Kelime Çalışma", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"
if "stats" not in st.session_state:
    st.session_state.stats = load_stats()
if "words" not in st.session_state:
    st.session_state.words = load_words()
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "total" not in st.session_state:
    st.session_state.total = 0

# ---------- Ana Sayfa ----------
if st.session_state.page == "home":
    st.title("📘 Vocabulary Trainer")

    if st.button("📝 Teste Başla"):
        st.session_state.page = "test"

    if st.button("📊 İstatistikler"):
        st.session_state.page = "stats"

    if st.button("📚 Kelimeler"):
        st.session_state.page = "words"

# ---------- Test Sayfası ----------
elif st.session_state.page == "test":
    st.header("📝 Genel Test")

    words = list(st.session_state.words.keys())
    if not words:
        st.warning("Hiç kelime yok, önce kelime ekleyin!")
        if st.button("⬅ Ana Sayfa"):
            st.session_state.page = "home"
    else:
        word = random.choice(words)
        st.write(f"**Kelime:** {word}")

        if st.button("Anlamını Göster"):
            st.success(f"Anlamı: {st.session_state.words[word]}")

        col1, col2 = st.columns(2)
        if col1.button("✅ Doğru"):
            st.session_state.correct += 1
            st.session_state.total += 1
        if col2.button("❌ Yanlış"):
            st.session_state.total += 1
            st.session_state.stats[word] = st.session_state.stats.get(word, 0) + 1
            save_stats(st.session_state.stats)

        if st.button("⬅ Ana Sayfa"):
            st.session_state.page = "home"

# ---------- İstatistik Sayfası ----------
elif st.session_state.page == "stats":
    st.header("📊 İstatistikler")
    total = st.session_state.total
    correct = st.session_state.correct
    if total > 0:
        st.write(f"Toplam Soru: {total}")
        st.write(f"Doğru: {correct}")
        st.write(f"Başarı: {correct/total*100:.1f}%")
    else:
        st.info("Henüz test yapılmadı.")

    st.subheader("En çok yanlış yapılanlar:")
    sorted_mistakes = sorted(st.session_state.stats.items(), key=lambda x: x[1], reverse=True)[:20]
    for word, count in sorted_mistakes:
        st.write(f"- {word}: {count} hata")

    if st.button("⬅ Ana Sayfa"):
        st.session_state.page = "home"

# ---------- Kelimeler Sayfası ----------
elif st.session_state.page == "words":
    st.header("📚 Kelime Listesi")
    for w, m in st.session_state.words.items():
        st.write(f"- **{w}**: {m}")

    st.subheader("➕ Yeni Kelime Ekle")
    eng = st.text_input("İngilizce kelime")
    tr = st.text_input("Türkçe anlamı")
    if st.button("Kaydet"):
        if eng and tr:
            st.session_state.words[eng] = tr
            save_words(st.session_state.words)
            st.success("Kelime eklendi!")
        else:
            st.warning("Lütfen her iki alanı doldurun!")

    if st.button("⬅ Ana Sayfa"):
        st.session_state.page = "home"
