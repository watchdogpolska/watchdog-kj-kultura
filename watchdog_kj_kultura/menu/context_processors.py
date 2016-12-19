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

        {% if menu %}
        <ul>
            {% for el in menu %}
            <li>
                <a href="{{el.url}}">{{el}}</a>
                {% if el.children_set %}
                <ul>
                {% for child in el.children_set %}
                    <li><a href="{{child.url}}">{{child}}</a>
                {% endfor %}
                </ul>
                {% endif %}
            </li>
            {% endfor %}
        </ul>
        {% endif %}

    """
    return {'menu': Element.objects.filter(parent=None).
            root_with_children().
            all()}
