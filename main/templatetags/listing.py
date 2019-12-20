from django.contrib.admin.views.main import (PAGE_VAR, ALL_VAR)
from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = Library()
DOT = '.'
FIRST = '.'
PREV = '.'
NEXT = '.'
LAST = '.'


@register.simple_tag
def paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == DOT:
        return '... '
    elif i == cl.page_num:
        return format_html('<li class="active"><a href="javascript:void(0);">{}</a></li> ', i + 1)
    else:
        return format_html('<li><a href="{}"{}>{}</a></li>',
                           cl.get_query_string({PAGE_VAR: i}),
                           mark_safe(' class="end"' if i == cl.paginator.num_pages - 1 else ''),
                           i + 1)


@register.inclusion_tag('admin/pagination.html')
def pagination(cl):
    """
    Generate the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page_num + 1

    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    pages = []
    curr_page = paginator.page(page_num)
    if pagination_required:
        ON_EACH_SIDE = 3

        # If there are less pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= ON_EACH_SIDE + 2:
            for pg_no in paginator.page_range:
                pages.append({
                    'text': pg_no,
                    'link': cl.get_query_string({PAGE_VAR: pg_no - 1}),
                    'class': 'active' if pg_no == page_num else ''
                })
        else:
            if page_num > ON_EACH_SIDE + 1:
                pages.append({
                    'text': '<i class="fa fa-angle-double-left"></i>',
                    'link': cl.get_query_string({PAGE_VAR: 0}),
                    'class': '',
                    'extra': 'title="First Page"'
                })

            if curr_page.has_previous():
                pages.append({
                    'text': '<i class="fa fa-angle-left"></i>',
                    'link': cl.get_query_string({PAGE_VAR: curr_page.previous_page_number() -1}),
                    'class': '',
                    'extra': 'title="Previous Page"'
                })

            if page_num > ON_EACH_SIDE:
                for pg_no in range(page_num - ON_EACH_SIDE, page_num + 1):
                    pages.append({
                        'text': pg_no,
                        'link': cl.get_query_string({PAGE_VAR: pg_no-1}),
                        'class': 'active' if pg_no == page_num else ''
                    })
            else:
                for pg_no in range(1, page_num + 1):
                    pages.append({
                        'text': pg_no,
                        'link': cl.get_query_string({PAGE_VAR: pg_no-1}),
                        'class': 'active' if pg_no == page_num else ''
                    })

            if page_num < (paginator.num_pages - ON_EACH_SIDE - 1):
                for pg_no in range(page_num + 1, page_num + ON_EACH_SIDE + 1):
                    pages.append({
                        'text': pg_no,
                        'link': cl.get_query_string({PAGE_VAR: pg_no-1}),
                        'class': 'active' if pg_no == page_num else ''
                    })
            else:
                for pg_no in range(page_num + 1, paginator.num_pages + 1):
                    pages.append({
                        'text': pg_no,
                        'link': cl.get_query_string({PAGE_VAR: pg_no-1}),
                        'class': 'active' if pg_no == page_num else ''
                    })

            if curr_page.has_next():
                pages.append({
                    'text': '<i class="fa fa-angle-right"></i>',
                    'link': cl.get_query_string({PAGE_VAR: curr_page.next_page_number()-1}),
                    'class': '',
                    'extra': 'title="Next Page"'
                })

            if page_num < (paginator.num_pages - ON_EACH_SIDE):
                pages.append({
                    'text': '<i class="fa fa-angle-double-right"></i>',
                    'link': cl.get_query_string({PAGE_VAR: paginator.num_pages-1}),
                    'class': '',
                    'extra': 'title="Last Page"'
                })

    page_detail_text = 'Showing {} to {} of {} {}'.format(
        curr_page.start_index(),
        curr_page.end_index(),
        paginator.count,
        cl.opts.verbose_name_plural
    )

    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'pages': pages,
        'page_detail_text': page_detail_text,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    }
