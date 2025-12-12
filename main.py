# -*- coding: utf-8 -*-

import sys
import os

# 🔧 تحقق من نظام التشغيل وضبط الترميز
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.kernel32.SetConsoleCP(65001)
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

from chatbot import AbsherChatbot

# 🚀 التشغيل
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 مرحباً بك في منصة أبشر الذكية")
    print("="*50)
    
    voice_choice = input("\nهل تريد تفعيل الصوت؟ (نعم/لا): ").strip().lower()
    voice_enabled = voice_choice in ['نعم', 'yes', 'y', '1']
    
    # إنشاء البوت مع أو بدون صوت
    bot = AbsherChatbot(voice_enabled=voice_enabled)
    
    # تشغيل البوت
    bot.run()