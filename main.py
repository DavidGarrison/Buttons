import buttons
import config

app = buttons.create_app(config)

# This is only used when running locally.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
