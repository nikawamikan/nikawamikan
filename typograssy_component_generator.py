import urllib
import colorsys

def hex_to_hsv(color: str) -> tuple[float, float, float]:
    color = color.lstrip("#")
    r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)

def hsv_to_hex(h: float, s: float, v: float) -> str:
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def mul_chroma(hsv:tuple[float, float, float], percent: int) -> tuple[float, float, float]:
    h, s, v = hsv
    return h, s*(percent/100), v

def mul_brightness(hsv:tuple[float, float, float], percent: int) -> tuple[float, float, float]:
    h, s, v = hsv
    tmp = 1 - v
    tmp *= percent/100
    tmp = 1 - tmp
    return h, s, tmp


class Typograssy:
    def __init__(
            self,
            text: str,
            comment: str = None,
            accent: str = None, 
            speed: int = 200,
        ) -> None:
        self._base_url = "https://typograssy.deno.dev/api?"
        self.params = {}
        if accent is not None:
            self.generate_colors(accent)
        self.add_param("text", text)
        self.add_param("speed", str(speed))
        if comment is not None:
            self.add_param("comment", comment)

    def add_param(self, param: str, value: str) -> None:
        self.params[param] = value

    def generate_colors(self, accent: str) -> None:
        h4 = hex_to_hsv(accent)

        h3 = mul_brightness(mul_chroma(h4, 80),80)
        h2 = mul_brightness(mul_chroma(h3, 60),60)
        h1 = mul_brightness(mul_chroma(h2, 50),50)
        h0 = mul_chroma(h2, 10)
        h0 = h0[0], h0[1], 0.95
        bg = mul_brightness(mul_chroma(h0, 20), 20)
        frame = mul_chroma(mul_brightness(h4, 50), 80)

        self.add_param("l0", hsv_to_hex(*h0))
        self.add_param("l1", hsv_to_hex(*h1))
        self.add_param("l2", hsv_to_hex(*h2))
        self.add_param("l3", hsv_to_hex(*h3))
        self.add_param("l4", hsv_to_hex(*h4))
        self.add_param("bg", hsv_to_hex(*bg))
        self.add_param("frame", hsv_to_hex(*frame))

    @property
    def url(self) -> str:
        return self._base_url + "&".join(
            [
                f"{k}={urllib.parse.quote(v)}" 
                for k, v in self.params.items()
            ]
        )

typograssy = Typograssy(
        text="ぐるぐるぐるぐる",
        comment="for(;;){System.out.print(\"ぐる\")}",
        accent="1cc9c4",
        speed=100,
    )
result = f"[![typograssy]({typograssy.url})](https://github.com/kawarimidoll/typograssy)"
print(result)
