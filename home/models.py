from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

# from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
# from wagtail.core.fields import StreamField
from streams import blocks

from wagtail.admin.edit_handlers import ObjectList, TabbedInterface

class HomePageCarouselImages(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    panels = [
        ImageChooserPanel("carousel_image"),
    ]
    

class HomePage(RoutablePageMixin,Page):
    templates = "home/home_page"
    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]
    max_count = 1

    banner_title = models.CharField(max_length=100, blank= True, null=True)
    banner_subtitle = RichTextField(features=["bold","italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content = StreamField(
        [
            
            ("cta", blocks.CTABlock()),
        ],
        null= True,
        blank = True
    )

    content_panels = Page.content_panels + [
       
        
        MultiFieldPanel([
            InlinePanel("carousel_images",max_num=5, min_num=1,label="Image"),
        ], heading= "Carousel Images"),
        
        StreamFieldPanel("content"),  
    ]

    banner_panels = [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                ImageChooserPanel("banner_image"),
                PageChooserPanel("banner_cta"),
            ], 
            heading= "Banner Options"
        ),
    ]

    # promote_panels = []
    # settings_panels = []

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading = 'Content'),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
            ObjectList(Page.settings_panels, heading= 'Settings Stuff'),
            ObjectList(banner_panels, heading="Banner Settings")
        ]
    )

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural= "Home Pages"

    @route(r'^subscribe/$') 
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['a_special_test'] = "Hello world 123123"
        return render(request, "home/subscribe.html", context)  