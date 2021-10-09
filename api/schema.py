import graphene

from graphene_django import DjangoObjectType, DjangoListField
from graphene import relay, ObjectType
from .models import Post,Category
from taggit.managers import TaggableManager
from graphene_django.converter import convert_django_field
from django.db.models import Q
from graphene import String, List

@convert_django_field.register(TaggableManager)
def convert_field_to_string(field, registry=None):
    return List(String, source='get_tags')


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")
        

class PostType(DjangoObjectType):
    synopsis = graphene.String(source = "synopsis")
    absolute_url= graphene.String(source = "get_absolute_url")
    created_ago= graphene.String(source = "created_ago")
    post_id = graphene.Int(source="get_id")
    class Meta:
        model = Post
        fields = ("__all__")
        #exclude = ("tags",)
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)

  
    all_posts = graphene.List(
        PostType,
        search=graphene.String(),
        categoryID=graphene.Int(),
        
        first=graphene.Int(),
        skip=graphene.Int(),
        
        orderby=graphene.String(),
        ordermode=graphene.String(),
    )
    #all_brand = DjangoFilterConnectionField(BrandType, orderBy=graphene.List(of_type=graphene.String))
	
    post_by_id = graphene.List(PostType, post_id=graphene.Int(required=True))

    post_by_slug = graphene.List(PostType, slug=graphene.String(required=True))

    post_by_category = graphene.List(PostType, categoryID=graphene.Int(required=True))
    
    def resolve_post_by_category(self, info,categoryID, **kwargs):
        qs= Post.objects.filter(category__id=categoryID).all()


        return  qs
        

    def resolve_post_by_slug(self, info,slug, **kwargs):
        return Post.objects.filter(slug=slug).all()

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_posts(self, info,search=None, first=None, skip=None,orderby=None,categoryID=None,ordermode="asc",**kwargs):
        
        qs = Post.objects.all()

        if(categoryID != None):
            qs=qs.filter(category=categoryID)
            
        if search != None:
            filter = (
                Q(title__icontains=search) |
                Q(post__icontains=search)
            )
            qs = qs.filter(filter)
        if(orderby):
            if(ordermode=="desc"):
                qs = qs.order_by(orderby).reverse()
            else:    
                qs = qs.order_by(orderby)
        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        
        
        return qs

    
    def resolve_post_by_id(self, info,post_id):
        return Post.objects.filter(id=post_id).all()

schema = graphene.Schema(query=Query)
