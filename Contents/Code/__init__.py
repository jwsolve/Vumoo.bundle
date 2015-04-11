######################################################################################
#
#	vumoo - v0.10
#
######################################################################################

TITLE = "Vumoo"
PREFIX = "/video/vumoo"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_MOVIES = "icon-tv.png"
ICON_LIST = "icon-list.png"
BASE_URL = "http://www.vumoo.ch"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_MOVIES)
	VideoClipObject.art = R(ART)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
	HTTP.Headers['Host'] = "www.vumoo.ch"
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	return Shows()

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/shows")	
def Shows():

	oc = ObjectContainer()
	html = HTML.ElementFromURL(BASE_URL + '/videos/category')

	for each in html.xpath("//div[@class='sb_dynamic expand_box']/ul/li"):
		title = each.xpath("./a/text()")[0]
		url = each.xpath("./a/@href")[0]

		oc.add(DirectoryObject(
			key = Callback(ShowEpisodes, title = title, url = url),
				title = title,
				thumb = ICON_LIST
				)
		)
	return oc

######################################################################################
@route(PREFIX + "/showepisodes")	
def ShowEpisodes(title, url):

	oc = ObjectContainer(title1 = title)
	html = HTML.ElementFromURL(BASE_URL + '/' + url)

	for each in html.xpath("//div[@class='panel-body']"):
		title = each.xpath("./a/@data-title")[0]
		url = each.xpath("./a/@href")[0]
		thumb = each.xpath("./a/img/@src")[0]
		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
				title = title,
				thumb = thumb
				)
		)
	return oc

######################################################################################
@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page = HTML.ElementFromURL(BASE_URL + url)
	title = page.xpath("//h3[@class='movie_title']/span/text()")[0]
	description = page.xpath("//div[contains(@class,'movie_detail_info')]/p/text()")[0].strip()
	thumb = page.xpath("//img[@class='mov_poster']/@src")[0]

	oc.add(VideoClipObject(
		title = title,
		summary = description,
		thumb = thumb,
		url = BASE_URL + '/' + url
		)
	)	
	
	return oc	
