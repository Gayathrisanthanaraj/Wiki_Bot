from flask import Flask, render_template, request
import wikipedia
from langdetect import detect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        detected_language = detect(name)
        p=[]
        p=name.split(' ')
        n = []
        for w in p:
            if w == 'in':
                break
            else:
                n.append(w)
        na = ' '.join(map(str, n))

        lan=['tamil','Tamil','english','English']

        for word in lan:
            if word in p:
                if word == 'tamil' or word == 'Tamil':
                    tam = 'ta'
                break
            else:
                tam='none'

        if detected_language == 'ta' and tam=='ta':
            wikipedia.set_lang('ta')
        elif detected_language == 'en' and tam=='ta':
            wikipedia.set_lang('ta')
        elif detected_language == 'ta':
            wikipedia.set_lang('ta')
        else:
            wikipedia.set_lang('en')
        try:
            opt=["line","sentence","lines","sentences"]
            for wor in opt:
                if wor in p:
                    sens = p.index(wor)
                    sen = sens - 1
                    pos = int(p[sen])
                    print(pos)
                    break

                else:
                    pos='none'
            if type(pos) == int:
                answer = wikipedia.summary(na,sentences=pos)
            else:
                answer = wikipedia.summary(na)
            return render_template('wikibot.html', name=name, answer=answer)
        except wikipedia.exceptions.PageError:
            error_message = "Page not found. Please enter a valid query."
            return render_template('wikibot.html', error_message=error_message)
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]  # Show the first 5 options for disambiguation
            error_message = "Ambiguous query. Please select a more specific term or refine your search."
            return render_template('wikibot.html', error_message=error_message, options=options)
    return render_template('wikibot.html')

if __name__ == '__main__':
    app.run(debug=True)
