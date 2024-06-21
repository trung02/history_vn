from django import template
import datetime

register = template.Library()

@register.filter
def reverse_list(value):
    return value[::-1]

@register.filter
def vietnamese_weekday(value):
    if isinstance(value, datetime.date):
        weekdays = {
            0: 'Thứ Hai',
            1: 'Thứ Ba',
            2: 'Thứ Tư',
            3: 'Thứ Năm',
            4: 'Thứ Sáu',
            5: 'Thứ Bảy',
            6: 'Chủ Nhật'
        }
        return weekdays[value.weekday()]
    return value