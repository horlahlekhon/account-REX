from project.app.models.business import Business

def save_biz(biz):
    biz = Business.get_object(biz)
    if not biz:
        business = Business(
            id = biz["id"],
            name = biz['name']
            owner =
        )