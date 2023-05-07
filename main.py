from flask import Flask, render_template, redirect, request
import string
import random
import json

app = Flask(__name__)
shortended_urls = {}

def gen_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = gen_short_url()
        while short_url in shortended_urls:
            short_url = gen_short_url()
        
        shortended_urls[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortended_urls, f)
        return render_template("shortened_url.html", url_root=request.url_root, short_url=short_url)
    # print(shortended_urls)
    return render_template("index.html", url_root=request.url_root, short_urls=shortended_urls)

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortended_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    
if __name__ == "__main__":
    with open("urls.json", "r") as f:
        shortended_urls = json.load(f)
    app.run(debug=True, port=5001)