from app.models import Question


def check_image_url_is_temporary_image_url(image_url: str):
    """
        # permanent image url = {form_id}/{image_url}
        # temporary image url = {form_id}/_{image_url}
    """
    image_url = image_url.split('/')[1]
    return image_url.startswith('_')


def turn_temporary_image_url_to_permanent_image_url(temporary_image_url: str):
    """
        # permanent image url = {form_id}/{image_url}
        # temporary image url = {form_id}/_{image_url}
    """
    folder = temporary_image_url.split('/')[0]
    image_url = temporary_image_url.split('/')[1]

    return f"{folder}/{image_url.split('_')[1]}"


def generate_existing_image_url_to_delete_and_new_image_url_to_update(
        question: Question,
        input_image_url
):
    # 原本的圖片網址
    existing_image_url = question.image_url if question.image_url else None

    # 判斷需不需要把 s3 圖片刪除 (有重新上傳圖片的時候才需要，)
    deletes_s3_by_image_url = check_image_url_is_temporary_image_url(input_image_url)

    if not deletes_s3_by_image_url:
        print('Not deletes_s3_by_image_url')

    # 處理要更新到 question 的圖片網址 (如果不是暫時網址，則維持原網址去更新 question)
    permanent_image_url = turn_temporary_image_url_to_permanent_image_url(
        temporary_image_url=input_image_url
    ) if deletes_s3_by_image_url else input_image_url

    return existing_image_url, deletes_s3_by_image_url, permanent_image_url
