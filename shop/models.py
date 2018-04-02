from django.db import models

# Create your models here.

# 제품, 카테고리

class Category(models.Model):
    # Depth카테고리 에 대해 알아보자.
    name = models.CharField(max_length=200, db_index=True)
    # allow_unicode : 한글 사용 가능하게 함.
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        # 커스텀admin페이지의 단수형 복수형 네임.
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # url pattern을 찾아서 해당하는 형태로 url 만들어서 변환
        from django.urls import reverse
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    # db_index: 디비 인덱싱 (검색속도와 연관)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    # decimal places: 소수점 2째자리까지 나타낸다.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    # on_sale = models.BooleanField(default=?) 판매중?

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        # index_together - > 데이터베이스에서 꺼내온 이후에 인덱스 값 측정
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('shop:product_detail', args=[self.id, self.slug])

