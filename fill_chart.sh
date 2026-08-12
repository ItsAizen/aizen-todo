#!/bin/bash

# تاریخ شروع و پایان
START_DATE="2026-07-12"
END_DATE="2026-08-12"

CURRENT_DATE="$START_DATE"

# حلقه برای پیمایش روزها
while [ "$CURRENT_DATE" != "$(date -d "$END_DATE + 1 day" +%Y-%m-%d)" ]; do
    # تولید تعداد کامیت تصادفی بین ۱ تا ۴ برای تنوع رنگ سبز
    NUM_COMMITS=$((1 + RANDOM % 4))
    
    for ((i=1; i<=NUM_COMMITS; i++)); do
        # ثبت تغییر در یک فایل لاگ
        echo "Activity log for $CURRENT_DATE - commit $i" >> history.log
        git add history.log
        
        # تولید ساعت تصادفی در طول روز
        HOUR=$(printf "%02d" $((8 + RANDOM % 12)))
        MINUTE=$(printf "%02d" $((RANDOM % 60)))
        COMMIT_DATE="${CURRENT_DATE}T${HOUR}:${MINUTE}:00"
        
        # ثبت کامیت با تاریخ سفارشی
        GIT_AUTHOR_DATE="$COMMIT_DATE" GIT_COMMITTER_DATE="$COMMIT_DATE" git commit -m "update: $CURRENT_DATE ($i)" --quiet
    done

    # رفتن به روز بعدی
    CURRENT_DATE=$(date -d "$CURRENT_DATE + 1 day" +%Y-%m-%d)
done

echo "کامیت‌ها با موفقیت ساخته شدند. در حال ارسال به گیت‌هاب..."
git push origin main
