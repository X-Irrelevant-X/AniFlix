from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import  *
from django import forms

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

#Samin
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Group)
admin.site.register(Contributor)


# Streaming
class AnimeRatingInline(admin.TabularInline):
    model = AnimeRating
    extra = 1

class GenreInline(admin.TabularInline):
    model = Anime.genres.through
    extra = 1
class AnimeAdminForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = '__all__'

    # Add a custom widget for the favorites field
    favorites = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Favorites', False),
        required=False,
    )

class FavoritesInline(admin.TabularInline):
    model = Anime.favorites.through
    extra = 1

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    form = AnimeAdminForm
    inlines = [AnimeRatingInline, GenreInline, FavoritesInline]
    list_display = ('name', 'studio', 'release_date', 'views')
    filter_horizontal = ('genres',)
    search_fields = ['name', 'studio']
    save_on_top = True
    save_as = True

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="595" height="842" />'.format(obj.image.url))
        else:
            return "No Image"

    image_tag.short_description = 'Image'

@admin.register(AnimeRating)
class AnimeRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'rating',)
    search_fields = ['user__username', 'anime__name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['anime', 'number', 'name', 'release_date']
    search_fields = ['name', 'anime__name']
    fields = ['name', 'number', 'release_date', 'anime', 'video_link']

    def video_link_display(self, obj):
        return f'<a href="{obj.video_link}" target="_blank">{obj.video_link}</a>'

    video_link_display.short_description = 'Video Link'
    video_link_display.allow_tags = True
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'episode', 'text', 'created_at',)
    search_fields = ['user__username', 'episode__name']