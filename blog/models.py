from django.db import models
from django.shortcuts import render  
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import(
    FieldPanel, 
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from streams import blocks
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
# Create your models here.

class BlogAuthorsOrderable(Orderable):
    page=  ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete= models.CASCADE,
    )
    panels = [
        SnippetChooserPanel("author"),
    ]



class BlogAuthor(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),

            ],
            heading = "Name and Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= "Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug to identify posts by this category",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]   

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name    

register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin,Page):

    template = "blog/blog_listing_page.html"
    max_count = 1
    subpage_types = ['blog.VideoBlogPage','blog.ArticleBlogPage', 'blog.BlogDetailPage']
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text= "Overwrites the default title",
    )
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request,*args,**kwargs)
        all_posts = BlogDetailPage.objects.live().public().order_by("-first_published_at")
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        paginator = Paginator(all_posts, 2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        #context["posts"] = BlogDetailPage.objects.live().public()
        #context['extra'] = "Read all about it"
        #context["regular_context_var"] = "hellooooo"
        #context["a_special_link"] = self.reverse_subpage("latest_posts")
        #context["authors"] = BlogAuthor.object.all()
        context["categories"] = BlogCategory.objects.all()
        return context 

    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request,*args,**kwargs)
        #context["posts"] = context["posts"][:1]
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:1]
        # context["name"] = "Ahmed San"
        # context["website"] = "snahmd.com"
        return render(request, "blog/latest_posts.html", context)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogDetailPage',
        related_name= 'tagged_items',
        on_delete=models.CASCADE,

    )


class BlogDetailPage(Page):

    subpage_types = []
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text= "Overwrites the default title",
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name = "+",
        on_delete= models.SET_NULL,
    )

    categories = ParentalManyToManyField("blog.BlogCategory",blank=True,)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null= True,
        blank = True
    )
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=0, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
               FieldPanel("categories", widget=forms.CheckboxSelectMultiple) 
            ],
            heading="Categories"
        ),
    ]

class ArticleBlogPage(BlogDetailPage):
    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100,
        blank=True, 
        null=True
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text= 'Best size for this image will be 1400x400'
    )
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        FieldPanel("tags"),
        ImageChooserPanel("banner_image"),
        ImageChooserPanel("intro_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=0, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
               FieldPanel("categories", widget=forms.CheckboxSelectMultiple) 
            ],
            heading="Categories"
        ),
    ]


class VideoBlogPage(BlogDetailPage):
    template = "blog/video_blog_page.html"
    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel("youtube_video_id"),
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
        
        StreamFieldPanel("content"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=0, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
               FieldPanel("categories", widget=forms.CheckboxSelectMultiple) 
            ],
            heading="Categories"
        ),
    ]