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

## Bug-03

Title
Bug: User cannot access to the Django admin panel.

Description
Expected: Redirect user to User authentication panel.
Actual: Redirect user to Django admin panel.

Steps you need
You can change you URL redirect in views.py or define it in settings.py.

## Bug-04

Title

claim_review_list function just uses login_required.

Descrption

Each user that enter to the website can see all of claim list, even if that person isn't claimer.

Serious problem in approv_reject_claim: each User can add claim_id to URL and approve or reject submit claims.

It'll cause revealing submit claim proof text and cause of changing info of others.

Steps you need

Check both function in view and try to change logic.

## Bug-05

Title:

Possibility to bypass device status rotation

Description:

In ItemForm, status field is active for submitting item and editing, As a result, the user can change the item's status directly, without going through `can_transition`; for example, they can set the item to 'closed' or 'delivered' during the registration process.

Impact: The state transition logic defined in `core/workflows.py` can be bypassed.

Steps you need:

## Bug-06

Title:

Possibility of approving multiple requests for a single vehicle

Description

Once a request is approved, the status of the item changes to `reviewing`; however, other pending requests remain eligible for approval.

The approval function does not verify whether the claim is still in a `pending` state, nor does it check if the item's current status permits approval.

Consequence: It is possible to approve multiple claimants for a single item.

Steps you need

## Bug-07

Title

The student ID number is not being recorded.

Description

The `student_id` field is defined in the registration form, but there is no corresponding field in the `User` model to store it.

Consequently, `form.save()` does not save this value to the database.

Result: The user enters a student ID, but the information cannot be retrieved later.

Steps you need

## Bug-08

Title

Location validation is incomplete.

Description

In `clean_location`, `description_check` is used instead of `location_check`. Consequently, the list of valid locations is not actually being checked.

Furthermore, the condition within `location_check` is written in reverse and needs to be corrected.

Steps you need

## Bug-09

Title

Possibility of a 500 error with invalid filters

Description

The `category`, `start_date`, and `end_date` parameters are passed directly into the QuerySet without sufficient validation.

For example, submitting `?category=abc` could trigger a 500 error when the category ID is being converted into a number.

Steps you need