from .models import Element


def menu(request):
    """A context processor which provide menu in ``menu`` template variable.

    Parameters
    ----------
    request : HttpRequest
        A django standard request object

    Example
    -------
    Menu render is very simple and effective. For example::

        <ul>
        {% for el in menu %}
        <li>
            <a href="{{el.url}}">{{el}}</a>
            <ul>
            {% for child in el.children %}
                <li><a href="{{el.url}}">{{el}}</a>
            {% endfor %}
            </ul>
        </li>
        {% endfor %}
        </ul>

    """
    return {'menu': Element.objects.root_with_children().all()}
