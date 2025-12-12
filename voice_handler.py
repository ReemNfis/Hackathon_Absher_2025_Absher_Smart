# -*- coding: utf-8 -*-

import pyttsx3
import speech_recognition as sr
from threading import Thread

class VoiceHandler:
    """معالج الصوت - تحويل صوت إلى نص والعكس"""
    
    def __init__(self):
        """تهيئة معالج الصوت"""
        
        # 🔊 محرك تحويل النص إلى صوت
        self.tts_engine = pyttsx3.init()
        
        # ضبط سرعة النطق
        self.tts_engine.setProperty('rate', 150)
        
        # ضبط مستوى الصوت
        self.tts_engine.setProperty('volume', 0.9)
        
        # اختيار الصوت العربي (إن أمكن)
        self.set_arabic_voice()
        
        # 🎤 محرك تحويل الصوت إلى نص
        self.recognizer = sr.Recognizer()
        
        # حساسية الميكروفون
        self.recognizer.energy_threshold = 4000
    
    # 🔊 دالة تعيين الصوت العربي
    def set_arabic_voice(self):
        """تحاول تعيين صوت عربي"""
        try:
            voices = self.tts_engine.getProperty('voices')
            
            # ابحث عن صوت عربي
            for voice in voices:
                if 'ar' in voice.languages:
                    self.tts_engine.setProperty('voice', voice.id)
                    print("✅ تم تعيين الصوت العربي")
                    return
            
            # إذا ما فاتت صوت عربي، استخدم الأول
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                print("⚠️  لا يوجد صوت عربي، سيتم استخدام الصوت الافتراضي")
        
        except Exception as e:
            print(f"⚠️  لم يتم تعيين الصوت: {e}")
    
    # 🔊 دالة تحويل النص إلى صوت
    def speak(self, text):
        """
        تحول النص إلى صوت وتشغله
        Input: النص (string)
        """
        try:
            print(f"🔊 جاري التحدث...")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        except Exception as e:
            print(f"❌ خطأ في تحويل النص إلى صوت: {e}")
    
    # 🎤 دالة تحويل الصوت إلى نص
    def listen(self, timeout=10):
        """
        تستمع للميكروفون وتحول الصوت إلى نص
        Input: timeout - الوقت الأقصى للاستماع (ثانية)
        Output: النص المعترف به
        """
        try:
            # استخدام الميكروفون
            with sr.Microphone() as source:
                print("🎤 جاري الاستماع... تحدث الآن!")
                
                # ضبط الضوضاء المحيطة
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # الاستماع للصوت
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
            
            # التعرف على الكلام
            print("🔍 جاري معالجة الصوت...")
            
            # جرب الخدمة الأولى (Google Speech Recognition - عربي)
            try:
                text = self.recognizer.recognize_google(audio, language='ar-SA')
                print(f"✅ تم التعرف: {text}")
                return text
            
            except sr.UnknownValueError:
                print("❌ لم أستطع فهم ما قلته، الرجاء المحاولة مرة أخرى")
                return None
            
            except sr.RequestError as e:
                print(f"❌ خطأ في الاتصال: {e}")
                return None
        
        except sr.RequestError:
            print("❌ لا يوجد اتصال بالإنترنت")
            return None
        
        except sr.UnknownValueError:
            print("❌ لم أستطع فهم الصوت")
            return None
        
        except Exception as e:
            print(f"❌ خطأ: {e}")
            return None
    
    # 🔊 دالة النطق بدون انتظار (غير متزامن)
    def speak_async(self, text):
        """
        تحول النص إلى صوت بدون انتظار
        يعمل في خيط منفصل
        """
        thread = Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
    
    # 🧪 دالة الاختبار
    def test(self):
        """اختبر معالج الصوت"""
        print("\n🧪 اختبار معالج الصوت:")
        print("="*50)
        
        # اختبار 1: تحويل نص إلى صوت
        print("\n1️⃣  اختبار Text to Speech:")
        self.speak("مرحبا، أنا أبشر الذكي")
        
        # اختبار 2: تحويل صوت إلى نص
        print("\n2️⃣  اختبار Speech to Text:")
        print("قل شيئاً في الميكروفون...")
        text = self.listen(timeout=5)
        if text:
            print(f"تم التعرف على: {text}")