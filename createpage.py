f = open('www/index.html', 'w')

h = open('www/header', 'r')
for line in h:
	f.write(line)

f.write('<div id="content">\n<h2>Home</h2>\n<p>\n')
f.write('This is my first webpage! I was able to code all the HTML and CSS in order to make it. Watch out world of web design here I come!')
f.write('</p>\n<p>\n') 
f.write('I can use my skills here to create websites for my business, my friends and family, my C.V, blog or articles. As well as any games or more experiment stuff (which is what the web is really all about).')
f.write('</p>\n</div>\n')

t = open('www/trailer', 'r')
for line in t:
	f.write(line)

f.close()
