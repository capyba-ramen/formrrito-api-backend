def turn_temporary_image_url_to_permanent_image_url(form_id: str, temporary_image_url: str):
    """
    # permanent image url = {form_id}/{image_url}
    # temporary image url = {form_id}/_{image_url}
    """
    return f"{form_id}/{temporary_image_url.split('_')[1]}"
