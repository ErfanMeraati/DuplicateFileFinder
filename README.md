# 🔍 Duplicate File Finder

**Day 4 of Daily Python Tools**

---

## 🇬🇧 English

A fast command-line tool that finds duplicate files in any folder — even if they have different names — using SHA256 hashing.

### ✨ Features
- Finds duplicates by content (SHA256), not just filename
- Pre-filters by file size for maximum speed
- Multi-threaded hashing with ThreadPoolExecutor
- Shows wasted disk space per group and total
- Supports drag & drop onto the `.exe`
- Option to save results to a timestamped `.txt` file

### 🚀 Usage

**Run the exe:**
DuplicateFileFinder.exe

Or drag a folder directly onto the exe.

Run with Python:

bash

python DuplicateFileFinder.py

or
python DuplicateFileFinder.py “C:\Users\You\Downloads”

📦 Requirements
No external packages needed — uses Python standard library only.

🖥️ Sample Output
============================================================ 🔍 Found 2 duplicate group(s)
[Group 1] — 3 copies | Size: 4.2 MB each | Wasted: 8.4 MB

Hash: a3f1c92b8e4d1f0a…📄 C:\Downloads\photo.jpg

🔁 C:\Backup\photo_copy.jpg

🔁 C:\Desktop\img_final.jpg

============================================================ 💾 Total wasted space: 8.4 MB
🇮🇷 فارسی
ابزاری سریع برای پیدا کردن فایل‌های تکراری در هر پوشه‌ای — حتی اگه اسمشون فرق داشته باشه.

✨ ویژگی‌ها
شناسایی تکراری‌ها بر اساس محتوا (SHA256)، نه اسم فایل
پیش‌فیلتر بر اساس سایز برای سرعت بیشتر
هش‌گذاری چندنخی با ThreadPoolExecutor
نمایش فضای هدررفته به ازای هر گروه و مجموع کل
پشتیبانی از drag & drop روی فایل exe
امکان ذخیره نتایج در فایل txt با تاریخ و ساعت
🚀 نحوه اجرا
اجرای exe:

DuplicateFileFinder.exe

یا یک پوشه رو مستقیم روی exe بکش و رها کن.

اجرا با پایتون:

bash

python DuplicateFileFinder.py

یا
python DuplicateFileFinder.py “C:\Users\شما\Downloads”

📦 نیازمندی‌ها
فقط کتابخانه‌های استاندارد پایتون — نیازی به نصب چیزی نیست.

🏗️ Build exe
bash

pip install pyinstaller

pyinstaller --onefile DuplicateFileFinder.py

Executable will be in the dist/ folder.

Part of the daily-python-tools series — one tool per day, getting better each time.
