import base64
url = f"""
http://mikan-box.imgix.net/bankan27.png
?fit=clip
&w=512
&txt-y=20
&txt64={base64.b64encode("かわちばんかん".encode()).decode()}
&txt-color=ffee00
&txt-line=2
&txt-line-color=404040
&txt-size=64
&txt-align=middle,center
""".replace(" ", "").replace("\n", "")

md_str = f"[![bankan]({url})](https://imgix.com)"
print(md_str)
