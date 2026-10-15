## BUG-01

Title:
کاربر می‌تواند Item کاربر دیگر را ویرایش کند.

Status:
- High
- Medium
- Low

Steps:
1. با user_a وارد شوید.
2. URL آیتم user_b را باز کنید.
3. /items/12/edit/

Expected:
دسترسی رد شود.

Actual:
فرم ویرایش نمایش داده می‌شود.

## BUG-02

Title:
صفحه home اول نمایش داده بشودو خطای 404 رفع گردد

Steps:
از قسمت url, urlpatterns آدرس دهی صحیح را انجام می‌دهیم.

Expected:
صفحه اصلی و لیست آیتم های گمشده را نمایش دهد.
Actual:
ارور 404 و عدم وجود این صفحه