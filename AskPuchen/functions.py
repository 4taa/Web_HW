from django.core.paginator import Paginator


def paginate(request, objects, objects_per_page=20):
    paginator = Paginator(objects, objects_per_page)
    page_num = request.GET.get('page')
    try:
        current_page = paginator.page(page_num)
    except:
        current_page = paginator.page(1)

    frame_size = 5
    half_frame_size = frame_size // 2
    page_num = current_page.number
    pages_count = paginator.num_pages
    if pages_count < frame_size:
        page_list = range(1, pages_count + 1)
    elif page_num <= half_frame_size:
        page_list = range(1, frame_size + 1)
    elif page_num >= (pages_count - half_frame_size):
        page_list = range(pages_count - frame_size, pages_count)
    else:
        page_list = range(page_num - half_frame_size, page_num + half_frame_size + 1)
    current_page.page_list = page_list
    return current_page
