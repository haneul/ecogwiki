# -*- coding: utf-8 -*-
import unittest2 as unittest
from models import PageOperationMixin


class RenderingTestCase(unittest.TestCase):
    def assertRenderedText(self, markdown, html):
        self.assertEqual(html, PageOperationMixin.render_body(u'Hello', markdown))


class SimpleExtensionsTest(RenderingTestCase):
    def setUp(self):
        super(SimpleExtensionsTest, self).setUp()

    def test_embedded_image_in_p(self):
        self.assertRenderedText(u'![Test](http://x.com/x.jpg)',
                                u'<p class="img-container"><img alt="Test" src="http://x.com/x.jpg"></p>')

    def test_embedded_image_in_li(self):
        self.assertRenderedText(u'*   ![Test](http://x.com/x.jpg)',
                                u'<ul>\n<li class="img-container"><img alt="Test" src="http://x.com/x.jpg"></li>\n</ul>')

    def test_strikethrough(self):
        self.assertRenderedText(u'Hello ~~AK~~?', u'<p>Hello <strike>AK</strike>?</p>')

    def test_partial_checkbox(self):
        self.assertRenderedText(u'[ ] Hello [x] There',
                                u'<p><input class="partial checkbox" type="checkbox"> Hello <input checked class="partial checkbox" type="checkbox"> There</p>')

    def test_partial_log(self):
        self.assertRenderedText(u'*   [__]',
                                u'<ul>\n<li>\n<form class="partial log"><input type="text"><input type="submit" value="Update"></form>\n</li>\n</ul>')

    def test_mathjax(self):
        self.assertRenderedText(u'Hello \\([[blah]]\\) There', u'<p>Hello \\([[blah]]\\) There</p>')

    def test_mathjax_inline(self):
        self.assertRenderedText(u'Hello\n$$\n[[blah]]\n$$\nThere', u'<p>Hello\n$$\n[[blah]]\n$$\nThere</p>')

    def test_table(self):
        self.assertRenderedText(u'| a | b |\n|---|---|\n| c | d |', u'<table>\n<thead>\n<tr>\n<th>a</th>\n<th>b</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td>c</td>\n<td>d</td>\n</tr>\n</tbody>\n</table>')

    def test_html(self):
        self.assertRenderedText(u'<div class="test">He*l*lo</div>\nWo*r*ld',
                                u'<div class="test">He*l*lo</div>\n\n<p>Wo<em>r</em>ld</p>')

    def test_html_sanitization(self):
        self.assertRenderedText(u'Hey<script>alert(1)</script>you', u'<p>Heyyou</p>')

    def test_underline_in_email(self):
        self.assertRenderedText(u'_akmail_@gmail.com', u'<p><a class="email" href="mailto:_akmail_@gmail.com">_akmail_@gmail.com</a></p>')
        self.assertRenderedText(u'http://x.com/_a_', u'<p><a class="plainurl" href="http://x.com/_a_">http://x.com/_a_</a></p>')
        self.assertRenderedText(u'![Image](http://x.com/_a_)', u'<p class="img-container"><img alt="Image" src="http://x.com/_a_"></p>')

    def test_leading_newlines_followed_by_schema_block(self):
        self.assertRenderedText(
            u'''\r\n\t#!yaml/schema\n    url: "http://abc.com"\n\nHello\n''',
            u'<p>Hello</p>')


class EmbedTest(RenderingTestCase):
    maxDiff = None

    def test_youtube(self):
        self.assertRenderedText(
            u'http://www.youtube.com/watch?v=w5gmK-ZXIMQ',
            u'<div class="video youtube"><iframe allowfullscreen="true" frameborder="0" height="390" scrolling="no" src="http://www.youtube.com/embed/w5gmK-ZXIMQ" width="640"></iframe></div>')

    def test_youtube2(self):
        self.assertRenderedText(
            u'<iframe width="640" height="390" src="//www.youtube.com/embed/w5gmK-ZXIMQ" frameborder="0" allowfullscreen></iframe>',
            u'<div class="video youtube2"><iframe allowfullscreen="true" frameborder="0" height="390" scrolling="no" src="http://www.youtube.com/embed/w5gmK-ZXIMQ" width="640"></iframe></div>')

    def test_vimeo(self):
        self.assertRenderedText(
            u'http://vimeo.com/1747316',
            u'<div class="video vimeo"><iframe allowfullscreen="true" frameborder="0" height="281" scrolling="no" src="http://player.vimeo.com/video/1747316" width="500"></iframe></div>')

    def test_vimeo2(self):
        self.assertRenderedText(
            u'<iframe src="//player.vimeo.com/video/1747316" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
            u'<div class="video vimeo2"><iframe allowfullscreen="true" frameborder="0" height="281" scrolling="no" src="http://player.vimeo.com/video/1747316" width="500"></iframe></div>')

    def test_ted(self):
        self.assertRenderedText(
            u'http://www.ted.com/talks/krista.html',
            u'<div class="video ted"><iframe allowfullscreen="true" frameborder="0" height="315" scrolling="no" src="http://embed.ted.com/talks/krista.html" width="560"></iframe></div>')

    def test_ted2(self):
        self.assertRenderedText(
            u'<iframe src="http://embed.ted.com/talks/krista.html" width="560" height="315" frameborder="0" scrolling="no" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>',
            u'<div class="video ted2"><iframe allowfullscreen="true" frameborder="0" height="315" scrolling="no" src="http://embed.ted.com/talks/krista.html" width="560"></iframe></div>')

    def test_prezi(self):
        self.assertRenderedText(
            u'http://prezi.com/sltlibmijbsv/copy-of-zoom-with-prezi/#',
            u'<div class="video prezi"><iframe allowfullscreen="true" frameborder="0" height="400" scrolling="no" src="http://prezi.com/embed/sltlibmijbsv/?bgcolor=ffffff&amp;lock_to_path=0&amp;autoplay=0&amp;autohide_ctrls=0&amp;features=undefined&amp;disabled_features=undefined" width="550"></iframe></div>')

    def test_prezi2(self):
        self.assertRenderedText(
            u'<iframe src="http://prezi.com/embed/sltlibmijbsv/?bgcolor=ffffff&amp;lock_to_path=0&amp;autoplay=0&amp;autohide_ctrls=0&amp;features=undefined&amp;disabled_features=undefined" width="550" height="400" frameBorder="0"></iframe>',
            u'<div class="video prezi2"><iframe allowfullscreen="true" frameborder="0" height="400" scrolling="no" src="http://prezi.com/embed/sltlibmijbsv/?bgcolor=ffffff&amp;lock_to_path=0&amp;autoplay=0&amp;autohide_ctrls=0&amp;features=undefined&amp;disabled_features=undefined" width="550"></iframe></div>')

    def test_google_calendar(self):
        self.assertRenderedText(
            u'<iframe src="https://www.google.com/calendar/embed?src=en.south_korea%23holiday%40group.v.calendar.google.com&ctz=Asia/Seoul" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>',
            u'<div class="video gcal"><iframe allowfullscreen="true" frameborder="0" height="600" scrolling="no" src="http://www.google.com/calendar/embed?src=en.south_korea%23holiday%40group.v.calendar.google.com&amp;ctz=Asia/Seoul" width="800"></iframe></div>')

    def test_slideshare(self):
        self.assertRenderedText(
            u'<iframe src="http://www.slideshare.net/slideshow/embed_code/29840080" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="https://www.slideshare.net/TerryJohnson9/top-10-benefits-of-using-slideshareslide-share" title="Top 10 Benefits of Using SlideShare" target="_blank">Top 10 Benefits of Using SlideShare</a> </strong> from <strong><a href="http://www.slideshare.net/TerryJohnson9" target="_blank">BZ9 :: Proven Marketing Solutions Since 2003</a></strong> </div>',
            u'<div class="video slideshare"><iframe allowfullscreen="true" frameborder="0" height="355" scrolling="no" src="http://www.slideshare.net/slideshow/embed_code/29840080" width="425"></iframe></div>')

    def test_google_map(self):
        self.assertRenderedText(
            u'https://maps.google.com/?ll=42.733593,-105.61172&spn=0.001147,0.002245&t=h&z=19',
            u'<div class="video googlemap"><iframe allowfullscreen="true" frameborder="0" height="350" scrolling="no" src="http://maps.google.com/?ll=42.733593,-105.61172&amp;spn=0.001147,0.002245&amp;t=h&amp;z=19&amp;output=embed" width="425"></iframe></div>')

    def test_google_map2(self):
        self.assertRenderedText(
            u'<iframe marginheight="0" marginwidth="0" src="https://maps.google.com/?ie=UTF8&amp;t=m&amp;ll=37.0625,-95.677068&amp;spn=24.455808,37.353516&amp;z=4&amp;output=embed"></iframe>',
            u'<div class="video googlemap2"><iframe allowfullscreen="true" frameborder="0" height="350" scrolling="no" src="http://maps.google.com/?ie=UTF8&amp;t=m&amp;ll=37.0625,-95.677068&amp;spn=24.455808,37.353516&amp;z=4&amp;output=embed" width="425"></iframe></div>')


class WikilinkTest(RenderingTestCase):
    def test_plain(self):
        self.assertRenderedText(u'[[heyyou]]', u'<p><a class="wikipage" href="/heyyou">heyyou</a></p>')

    def test_space(self):
        self.assertRenderedText(u'[[Hey you]]', u'<p><a class="wikipage" href="/Hey_you">Hey you</a></p>')

    def test_special_character(self):
        self.assertRenderedText(u'[[너 & 나]]', u'<p><a class="wikipage" href="/%EB%84%88_%26_%EB%82%98">너 &amp; 나</a></p>')

    def test_possible_conflict_with_plain_link(self):
        self.assertRenderedText(u'[[Hello]](there)', u'<p><a class="wikipage" href="/Hello">Hello</a>(there)</p>')

    def test_dates(self):
        self.assertRenderedText(u'[[1979-03-05]]',
                                u'<p><time datetime="1979-03-05"><a class="wikipage" href="/1979">1979</a><span>-</span><a class="wikipage" href="/March_5">03-05</a></time></p>')
        self.assertRenderedText(u'[[1979-03-??]]',
                                u'<p><time datetime="1979-03-??"><a class="wikipage" href="/1979">1979</a><span>-</span><a class="wikipage" href="/March">03-??</a></time></p>')
        self.assertRenderedText(u'[[1979-??-??]]',
                                u'<p><time datetime="1979-??-??"><a class="wikipage" href="/1979">1979</a><span>-</span><span>??-??</span></time></p>')
        self.assertRenderedText(u'[[1979-03-05 BCE]]',
                                u'<p><time datetime="1979-03-05 BCE"><a class="wikipage" href="/1979_BCE">1979</a><span>-</span><a class="wikipage" href="/March_5">03-05</a><span> BCE</span></time></p>')

    def test_url(self):
        markdowns = [
            u'http://x.co',
            u'(http://x.co)',
            u'http://x.co에',
            u'http://x.co?y',
            u'codeRepository::http://x.co',
            u'a@x.com',
            u'a@x.kr에',
        ]
        htmls = [
            u'<p><a class="plainurl" href="http://x.co">http://x.co</a></p>',
            u'<p>(<a class="plainurl" href="http://x.co">http://x.co</a>)</p>',
            u'<p><a class="plainurl" href="http://x.co">http://x.co</a>에</p>',
            u'<p><a class="plainurl" href="http://x.co?y">http://x.co?y</a></p>',
            u'<p><a class="plainurl" href="http://x.co" itemprop="codeRepository">http://x.co</a></p>',
            u'<p><a class="email" href="mailto:a@x.com">a@x.com</a></p>',
            u'<p><a class="email" href="mailto:a@x.kr">a@x.kr</a>에</p>',
        ]

        for markdown, html in zip(markdowns, htmls):
            self.assertRenderedText(markdown, html)


class SchemaItemPropertyRenderingTest(RenderingTestCase):
    def test_isbn(self):
        self.assertRenderedText(
            u'{{isbn::0618680004}}',
            u'<p><a class="isbn" href="http://www.amazon.com/gp/product/0618680004" itemprop="isbn">0618680004</a></p>'
        )

    def test_isbn_kr(self):
        self.assertRenderedText(
            u'{{isbn::8936437267}}',
            u'<p><a class="isbn" href="http://www.aladin.co.kr/shop/wproduct.aspx?ISBN=9788936437267" itemprop="isbn">9788936437267</a></p>'
        )

    def test_isbn13_kr(self):
        self.assertRenderedText(
            u'{{isbn::9788936437267}}',
            u'<p><a class="isbn" href="http://www.aladin.co.kr/shop/wproduct.aspx?ISBN=9788936437267" itemprop="isbn">9788936437267</a></p>'
        )

    def test_generic_key_value(self):
        self.assertRenderedText(
            u'{{hello::world from ak}}',
            u'<p><span itemprop="hello">world from ak</span></p>'
        )

    def test_class(self):
        self.assertRenderedText(
            u'{{.hello::world from ak}}',
            u'<p><span class="hello">world from ak</span></p>'
        )


class SectionRenderingTest(RenderingTestCase):
    def test_simple(self):
        self.assertRenderedText(
            u'description::---\n\nHello\n',
            u'<div class="section" itemprop="description">\n<p>Hello</p>\n</div>'
        )

    def test_section_containing_multiple_blocks(self):
        self.assertRenderedText(
            u'description::---\n\nHello\n\nTh*e*re',
            u'<div class="section" itemprop="description">\n<p>Hello</p>\n<p>Th<em>e</em>re</p>\n</div>'
        )

    def test_multiple_sections(self):
        self.assertRenderedText(
            u'description::---\n\nHello\n\naward::---\n\nThere\n',
            u'<div class="section" itemprop="description">\n<p>Hello</p>\n</div>\n<div class="section" itemprop="award">\n<p>There</p>\n</div>'
        )
