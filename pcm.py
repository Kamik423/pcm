#!/usr/bin/env python3
"""Generate a graphic for post and comment flair distribution and percentage of
wall of text posts.

Attributes:
    APPLICATION_CONFIG (pathlib.Path): The config file holding the reddit access
        information formated as yaml:

            client_id: asdf
            client_secret: fdsa
            password: swordfish
            user_agent: PCM
            username: me

    SCRIPT (pathlib.Path): The path of the currently running file.
    SCRIPTDIR (pathlib.Path): The directory the config and the python file are
        located in.
"""

import itertools
from datetime import date
from math import sqrt
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import praw
import yaml
from tqdm import tqdm

SCRIPT = Path(__file__)
SCRIPTDIR = SCRIPT.parent
APPLICATION_CONFIG = SCRIPTDIR / "app.yaml"


def pcm(
    axes: matplotlib.axes.Axes,
    center: float,
    auth: float,
    authleft: float,
    left: float,
    libleft: float,
    lib: float,
    libright: float,
    right: float,
    authright: float,
    unflaired: float,
    center_label: str = "",
    auth_label: str = "",
    authleft_label: str = "",
    left_label: str = "",
    libleft_label: str = "",
    lib_label: str = "",
    libright_label: str = "",
    right_label: str = "",
    authright_label: str = "",
    unflaired_label: str = "",
    label: bool = False,
) -> None:
    """Draw a political compass size diagram into a given axes.

    Args:
        axes (matplotlib.axes.Axes): The axes to draw into.
        center (float): The size of the center patch.
        auth (float): The size of the autoritarian patch.
        authleft (float): The size of the authleft patch.
        left (float): The size of the left patch.
        libleft (float): The size of the libleft patch.
        lib (float): The size of the liberal patch.
        libright (float): The size of the libright patch.
        right (float): The size of the right patch.
        authright (float): The size of the authright patch.
        unflaired (float): The size of the unflaired patch.
        center_label (str, optional): The label for the center patch.
        auth_label (str, optional): The label for the authoritarian patch.
        authleft_label (str, optional): The label for the authleft patch.
        left_label (str, optional): The label for the left patch.
        libleft_label (str, optional): The label for the libleft patch.
        lib_label (str, optional): The label for the liberal patch.
        libright_label (str, optional): The label for the libright patch.
        right_label (str, optional): The label for the right patch.
        authright_label (str, optional): The label for the authright patch.
        unflaired_label (str, optional): The label for the unflaired patch.
        label (bool, optional): Label the sectors with their name.
    """
    # avoid crashes if center is 0
    true_center = center
    if center == 0:
        center = (
            sum(
                [
                    auth,
                    authleft,
                    left,
                    libleft,
                    lib,
                    libright,
                    right,
                    authright,
                    unflaired,
                ]
            )
            / 9
        )
        if center == 0:
            center = 1

    # Draw patches
    patches = [
        matplotlib.patches.Rectangle(
            (-0.5, -0.5), true_center / center, true_center / center
        ),
        matplotlib.patches.Rectangle((-0.5, 0.5), 1, auth / center),
        matplotlib.patches.Rectangle(
            (-0.5, 0.5), -sqrt(authleft / center), sqrt(authleft / center)
        ),
        matplotlib.patches.Rectangle((-0.5, -0.5), -left / center, 1),
        matplotlib.patches.Rectangle(
            (-0.5, -0.5), -sqrt(libleft / center), -sqrt(libleft / center)
        ),
        matplotlib.patches.Rectangle((-0.5, -0.5), 1, -lib / center),
        matplotlib.patches.Rectangle(
            (0.5, -0.5), sqrt(libright / center), -sqrt(libright / center)
        ),
        matplotlib.patches.Rectangle((0.5, -0.5), right / center, 1),
        matplotlib.patches.Rectangle(
            (0.5, 0.5), sqrt(authright / center), sqrt(authright / center)
        ),
        matplotlib.patches.Rectangle(
            (
                0.75
                + max(
                    right / center,
                    sqrt(libright / center),
                    sqrt(authright / center),
                ),
                -0.5 * sqrt(unflaired / center),
            ),
            sqrt(unflaired / center),
            sqrt(unflaired / center),
        ),
    ]
    colors = [
        "#c3c3c3",
        "#a190ba",
        "#ff7575",
        "#cdb187",
        "#9aed98",
        "#c8f185",
        "#f5f471",
        "#9ccfb8",
        "#42aaff",
        "#3c3c3c",
    ]

    patches_collection = matplotlib.collections.PatchCollection(
        patches, cmap=matplotlib.colors.ListedColormap(colors)
    )
    patches_collection.set_array(np.arange(11))
    axes.add_collection(patches_collection)

    # Draw labels
    axes.text(
        0,
        0,
        center_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        0,
        0.5 + 0.5 * auth / center,
        auth_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        -0.5 - 0.5 * sqrt(authleft / center),
        0.5 + 0.5 * sqrt(authleft / center),
        authleft_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        -0.5 - 0.5 * left / center,
        0,
        left_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        -0.5 - 0.5 * sqrt(libleft / center),
        -0.5 - 0.5 * sqrt(libleft / center),
        libleft_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        0,
        -0.5 - 0.5 * lib / center,
        lib_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        0.5 + 0.5 * sqrt(libright / center),
        -0.5 - 0.5 * sqrt(libright / center),
        libright_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        0.5 + 0.5 * right / center,
        0,
        right_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        0.5 + 0.5 * sqrt(authright / center),
        0.5 + 0.5 * sqrt(authright / center),
        authright_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
    )
    axes.text(
        0.75
        + max(
            right / center,
            sqrt(libright / center),
            sqrt(authright / center),
        )
        + 0.5 * sqrt(unflaired / center),
        0,
        unflaired_label,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=8,
        color="#ffffff",
    )

    # Draw name labels

    if label:
        axes.arrow(0, 0.75 + auth / center, 0, -0.15, width=0.02, facecolor="black")
        axes.annotate(
            "Authoritarian",
            (0, 0.75 + auth / center),
            horizontalalignment="center",
            verticalalignment="bottom",
        )

        axes.arrow(
            -1 - sqrt(authleft / center),
            1 + sqrt(authleft / center),
            0.4,
            -0.4,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "AuthLeft",
            (-1 - sqrt(authleft / center), 1 + sqrt(authleft / center)),
            horizontalalignment="right",
            verticalalignment="bottom",
        )

        axes.arrow(
            -1 - left / center,
            0.5,
            0.4,
            -0.1,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "Left",
            (-1 - left / center, 0.5),
            horizontalalignment="right",
            verticalalignment="center",
        )

        axes.arrow(
            -0.8 - left / center,
            -0.4,
            0.2 + left / center,
            0.1,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "Centrist",
            (-0.8 - left / center, -0.4),
            horizontalalignment="right",
            verticalalignment="center",
        )

        axes.arrow(
            -1 - sqrt(libleft / center),
            -1 - sqrt(libleft / center),
            0.4,
            0.4,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "LibLeft",
            (-1 - sqrt(libleft / center), -1 - sqrt(libleft / center)),
            horizontalalignment="right",
            verticalalignment="top",
        )

        axes.arrow(
            0,
            -0.75 - lib / center,
            0,
            0.15,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "Liberal",
            (0, -0.75 - lib / center),
            horizontalalignment="center",
            verticalalignment="top",
        )

        axes.arrow(
            1 + sqrt(libright / center),
            -1 - sqrt(libright / center),
            -0.4,
            0.4,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "LibRight",
            (1 + sqrt(libright / center), -1 - sqrt(libright / center)),
            horizontalalignment="left",
            verticalalignment="top",
        )

        axes.arrow(
            1 + right / center,
            0.75 * sqrt(unflaired / center),
            -0.4,
            min(0.4 - 0.75 * sqrt(unflaired / center), -0.1),
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "Right",
            (1 + right / center, 0.75 * sqrt(unflaired / center)),
            horizontalalignment="left",
            verticalalignment="bottom",
        )

        axes.arrow(
            1 + sqrt(authright / center),
            1 + sqrt(authright / center),
            -0.4,
            -0.4,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "AuthRight",
            (1 + sqrt(authright / center), 1 + sqrt(authright / center)),
            horizontalalignment="left",
            verticalalignment="bottom",
        )

        axes.arrow(
            1
            + max(right / center, sqrt(libright / center), sqrt(authright / center))
            + 0.5 * sqrt(unflaired / center),
            -0.5 - 0.5 * sqrt(unflaired / center),
            -0.05,
            0.4,
            width=0.02,
            facecolor="black",
        )
        axes.annotate(
            "Unflaired",
            (
                1
                + max(right / center, sqrt(libright / center), sqrt(authright / center))
                + 0.5 * sqrt(unflaired / center),
                -0.5 - 0.5 * sqrt(unflaired / center),
            ),
            horizontalalignment="center",
            verticalalignment="top",
        )

    # Limit plot size and do layouting stuff

    axes.set_ylim(
        -0.5
        - max(
            lib / center,
            sqrt(libright / center),
            sqrt(libleft / center),
        ),
        0.5
        + max(
            auth / center,
            sqrt(authright / center),
            sqrt(authleft / center),
        ),
    )
    axes.set_xlim(
        -0.5
        - max(
            left / center,
            sqrt(libleft / center),
            sqrt(authleft / center),
        )
        - 0.5,  # bonus pad,
        1
        + max(
            right / center,
            sqrt(libright / center),
            sqrt(authright / center),
        )
        + sqrt(unflaired / center),
    )

    axes.axis("equal")
    # axes.set_axis_off() # removed since I need y labels

    axes.tick_params(
        top=False,
        bottom=False,
        left=False,
        right=False,
        labelleft=False,
        labelbottom=False,
        pad=0,
        grid_linewidth=0,
    )
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.spines["left"].set_visible(False)
    axes.spines["bottom"].set_visible(False)


def reddit_from_json() -> praw.Reddit:
    """Creates a reddit object generated from the application config.

    Returns:
        praw.Reddit: a reddit object.
    """
    userdata = yaml.load(APPLICATION_CONFIG.read_text(), Loader=yaml.FullLoader)
    return praw.Reddit(
        client_id=userdata["client_id"],
        client_secret=userdata["client_secret"],
        password=userdata["password"],
        user_agent=userdata["user_agent"],
        username=userdata["username"],
    )


def get_flair_index(flair_text: str) -> int:
    """Get the index of a flair in my default list from a flair name.

    0: Centrist
    1: Autoritarian
    2: AuthLeft
    3: Left
    4: LibLeft
    5: Liberal
    6: LibRight
    7: Right
    8: AuthRight
    9: Unflaired

    Args:
        flair_text (str): The flair name.

    Returns:
        int: The flair/quadrant index.

    Raises:
        RuntimeError: If the flair name is unknown.
    """
    flair = (
        flair_text.split(":")[1]
        if flair_text is not None and flair_text.count(":") >= 2
        else flair_text
    )
    if flair in ["centrist", "CENTG"]:
        return 0
    elif flair == "auth":
        return 1
    elif flair == "authleft":
        return 2
    elif flair == "left":
        return 3
    elif flair == "libleft":
        return 4
    elif flair == "lib":
        return 5
    elif flair in ["libright", "libright2"]:
        return 6
    elif flair == "right":
        return 7
    elif flair == "authright":
        return 8
    elif flair in ["", "Undecided/Exploring", "user_flair_PolComp", "\u200e", None]:
        return 9
    else:
        raise RuntimeError(f"flair {repr(flair_text)} unknown")


def count_flairs(flair_texts: list[str]) -> list[int]:
    """Return the amount of times a quadrant has occurs in a list of flair names.

    Args:
        flair_texts (list[str]): The flair names.

    Returns:
        list[int]: The amount of times each quadrant occurs, indices taken from
            get_flair_index() above.
    """
    accumulator = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for flair_text in flair_texts:
        accumulator[get_flair_index(flair_text)] += 1
    return accumulator


def get_flairs(subreddit_name: str, mode: int, count: int) -> list[int]:
    """Get the amount of times a quadrant has been flaired in some posts or
    comments as described by the arguments.

    Args:
        subreddit_name (str): The name of the subreddit to search.
        mode (int): The mode. 0=hot, 1=top, 2=comments on newest posts.
        count (int): The amount of posts to look at. If the mode is "comments"
            there will still be `count` posts searched, looking at all their
            comments.

    Returns:
        list[int]: The amount of times each quadrant occurs, indices taken from
            get_flair_index() above.
    """
    reddit = reddit_from_json()
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    if mode == 0:
        posts = subreddit.hot(limit=count)
    elif mode == 1:
        posts = subreddit.top(limit=count)
    elif mode == 2:
        posts = itertools.chain(
            *[post_.comments for post_ in subreddit.new(limit=count)]
        )
    posts_ = []
    for post in posts:
        try:
            posts_.append(post.author_flair_text)
        except AttributeError:
            pass
    flairs = count_flairs(posts_)
    return flairs


def word_count(string: str) -> int:
    """Count the words in a string. Might not be 100% correct.

    Args:
        string (str): The string to analyze.

    Returns:
        int: The word count.
    """
    return string.count(" ") + string.replace("\n\n", "\n").count("\n") + 1


def get_average_comment_length(
    subreddit_name: str, count: int
) -> tuple[list[float], int]:
    """Get the average comment length in a subreddit.

    It searches the newest posts.

    Args:
        subreddit_name (str): The name of the subreddit.
        count (int): The amount of posts to look at.

    Returns:
        list[float]: The average comment length for each quadrant. Indices
            taken from get_flair_index() above.
        int: The total amount of comments searched.
    """
    reddit = reddit_from_json()
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=count)
    comment_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    accumulated_length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for post in posts:
        for comment in post.comments:
            try:
                index = get_flair_index(comment.author_flair_text)
            except AttributeError:
                continue
            comment_count[index] += 1
            accumulated_length[index] += word_count(comment.body)
    return (
        [
            float(total) / float(count) if count else 0
            for total, count in zip(accumulated_length, comment_count)
        ],
        sum(comment_count),
    )


def get_wall_of_text_fraction(
    subreddit_name: str, count: int, threshold: int
) -> tuple[list[float], int]:
    """The fraction of comments in each quadrant that are percieved as a wall
    of text.

    It searches the newest posts.

    Args:
        subreddit_name (str): The name of the subreddit.
        count (int): The amount of posts to look at.
        threshold (int): The amount of words at which point a post is percieved
            as being a wall of text.

    Returns:
        list[float]: The fraction of comments in each quadrant percieved as a
            wall of text. Indices taken from get_flair_index() above.
        int: The total amount of comments searched.
    """
    reddit = reddit_from_json()
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=count)
    comment_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    walls_of_text = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for post in posts:
        for comment in post.comments:
            try:
                index = get_flair_index(comment.author_flair_text)
            except AttributeError:
                continue
            comment_count[index] += 1
            walls_of_text[index] += word_count(comment.body) > threshold
    return (
        [
            float(walls) / float(count) if count else 0
            for walls, count in zip(walls_of_text, comment_count)
        ],
        sum(comment_count),
    )


def main() -> None:
    """The main function generating the plot and subplots."""
    subreddits = ["PoliticalCompass", "PoliticalCompassMemes"]
    figure, axes = plt.subplots(len(subreddits), 5, figsize=(17, 6))
    count = 500
    wall_of_text = 100
    plt.tight_layout(h_pad=-1, w_pad=-1.5)
    progress = tqdm(total=len(subreddits) * 5)
    for subreddit_index, subreddit_name in enumerate(subreddits):
        axis = axes[subreddit_index, 0]
        axis.set_ylabel(f"r/{subreddit_name}", fontsize=14, labelpad=10)
        if subreddit_name == subreddits[0]:
            axis.set_title("Hot", fontsize=14)
        results = get_flairs(subreddit_name, 0, count)
        if sum(results):
            pcm(
                axis,
                *[result / sum(results) for result in results],
                *[f"{100.0 * result / sum(results):.1f}%" for result in results],
            )
        axis.set_xlabel(f"Latest {sum(results)} posts", fontsize=8)
        progress.update(1)

        axis = axes[subreddit_index, 1]
        if subreddit_name == subreddits[0]:
            axis.set_title("Top", fontsize=14)
        results = get_flairs(subreddit_name, 1, count)
        if sum(results):
            pcm(
                axis,
                *[result / sum(results) for result in results],
                *[f"{100.0 * result / sum(results):.1f}%" for result in results],
            )
        axis.set_xlabel(f"Latest {sum(results)} posts", fontsize=8)
        progress.update(1)

        axis = axes[subreddit_index, 2]
        if subreddit_name == subreddits[0]:
            axis.set_title("Comments", fontsize=14)
        results = get_flairs(subreddit_name, 2, count)
        if sum(results):
            pcm(
                axis,
                *[result / sum(results) for result in results],
                *[f"{100.0 * result / sum(results):.1f}%" for result in results],
            )
        axis.set_xlabel(f"Latest {sum(results)} comments", fontsize=8)
        progress.update(1)

        axis = axes[subreddit_index, 3]
        if subreddit_name == subreddits[0]:
            axis.set_title("Comment Length [words]", fontsize=14)
        results, comment_count = get_average_comment_length(subreddit_name, count)
        pcm(axis, *results, *[f"{result:.1f}" for result in results])
        axis.set_xlabel(f"{comment_count} comments on latest posts", fontsize=8)
        progress.update(1)

        axis = axes[subreddit_index, 4]
        if subreddit_name == subreddits[0]:
            axis.set_title(r"%age comments are wall of text", fontsize=14)
        results, comment_count = get_wall_of_text_fraction(
            subreddit_name, count, wall_of_text
        )
        pcm(
            axis,
            *results,
            *[fr"{100 * result:.1f}%" for result in results],
            label=subreddit_name == subreddits[-1],
        )
        axis.set_xlabel(f"{comment_count} comments on latest posts", fontsize=8)
        progress.update(1)

    figure.suptitle(
        "Flair distribution on posts and comments and average comment length",
        fontsize=15,
    )
    plt.subplots_adjust(top=0.875, bottom=0.065, left=0.04, right=0.99)
    figure.supxlabel(
        f"Wall of text for >{wall_of_text} words. "
        "https://github.com/Kamik423/pcm "
        f"{date.today()}",
        fontsize=8,
    )
    figure.savefig("pcm.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    main()
