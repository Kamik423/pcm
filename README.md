# Political Compass Subreddit Analyzer

![graphic](pcm.png)

Generate this graphic for a named list of subreddits.
The code is well documented.
PRs welcome.

Originally inspired by [this reddit post](https://www.reddit.com/r/PoliticalCompassMemes/comments/qa03zu/which_quadrant_is_most_likely_to_respond_with_a/).

## Setup

Have Python installed.
Install packages as follows:

```bash
pip install -r requirements.txt
```

Create the file `app.yaml` in the same directory containing your [access information](https://www.reddit.com/prefs/apps/).
The file should look like this:

```yaml
client_id: asdf
client_secret: fdsa
password: swordfish
user_agent: PCM
username: me
```

## Execution

```bash
./pcm.py
```

## License

MIT

