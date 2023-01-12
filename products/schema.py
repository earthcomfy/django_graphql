import graphene
from graphene_django import DjangoObjectType

from .models import Price, Product, ProductTag


class ProductTagType(DjangoObjectType):
    class Meta:
        model = ProductTag
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class PriceType(DjangoObjectType):
    class Meta:
        model = Price
        fields = "__all__"


class Query(graphene.ObjectType):
    tags = graphene.List(ProductTagType)
    products = graphene.List(ProductType)
    prices = graphene.List(PriceType)

    def resolve_tags(root, info):
        return ProductTag.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_prices(root, info):
        return Price.objects.all()


class CreateProductTag(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    product_tag = graphene.Field(ProductTagType)

    def mutate(root, info, name):
        product_tag = ProductTag(name=name)
        product_tag.save()
        return CreateProductTag(product_tag=product_tag)


class UpdateProductTag(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String(required=True)

    product_tag = graphene.Field(ProductTagType)

    def mutate(root, info, id, name):
        tag = ProductTag.objects.get(id=id)
        tag.name = name
        return UpdateProductTag(product_tag=tag)


class DeleteProductTag(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        ProductTag.objects.get(id=id).delete()
        return DeleteProductTag(ok=True)


class Mutation(graphene.ObjectType):
    create_product_tag = CreateProductTag.Field()
    update_product_tag = UpdateProductTag.Field()
    delete_product_tag = DeleteProductTag.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
