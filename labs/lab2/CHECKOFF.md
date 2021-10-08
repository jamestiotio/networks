# SUTD 2021 50.012 Networks Lab 2 Checkoff Submission README Document

> James Raphael Tiovalen / 1004555

## Inspiration

As background context, this API was inspired by [Spamton](https://deltarune.fandom.com/wiki/Spamton), an eccentric item shop vendor character in [Deltarune](https://deltarune.com/) (a video game created/developed by [Toby Fox](https://twitter.com/tobyfox) and his team).

## Setup Usage Instructions

Firstly, make sure that you have the [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) pre-requisites installed on your machine.

Simply change/set your current directory to the directory where this [`CHECKOFF.md`](./CHECKOFF.md) file resides and run the command `docker-compose up` to set up the REST API server. When you visit [http://127.0.0.1:8000](http://127.0.0.1:8000), you should be able to see/get some output.

## Endpoints Documentation

This is the list of endpoints provided in this REST API, as well as how to use them and their expected responses, categorized by their corresponding methods.

### GET

All of these endpoints under this section are idempotent, and most of them require authorization to identify the player's current character (except `/characters`, which is only simply idempotent).

1. `/fortunes`

Get a fortune.

2. `/weapons`

Check your list of weapons.

3. `/armors`

Check your list of armors.

4. `/spells`

Check your list of spells.

5. `/characters`

Get a list of available characters. Accepts `sortId`, `count` and `offset` query parameters.

6. `/stories`

Get some juicy lore about Photron. If you are authorized, perhaps you can learn a secret or two?

### POST

All of these endpoints under this section require authorization to identify the player's current character.

1. `/weapons`

Buy offensive weapons to attack enemies.

2. `/armors`

Buy defensive armors to protect yourself.

3. `/spells`

Buy magic spells to cast special effects.

4. `/kromers`

Donate some Kromers to Photron to make him happy. Has a low chance of obtaining a special item, which subtly increases the more Kromers are donated.

5. `/dark_dollars`

Donate some Dark Dollars to Photron to make him happy.

6. `/characters`

Add or create new characters. While POST requests are generally non-idempotent, the implementation of this endpoint allows us to preserve idempotency since it checks for existing character IDs.

### PUT

All of these endpoints under this section are idempotent.

1. `/characters/{character_id}`

Update your character's details.

### DELETE

All of these endpoints under this section are idempotent, and most require authorization to identify the player's current character (except `/characters`, which is only simply idempotent).

1. `/items`

Throw away an item that you own. It can be either a weapon, an armor, or a spell. Once discarded, an item can never be retrieved back.

2. `/kromers`

Remove some Kromers from yourself for some reason. Has a low chance of inflicting a negative effect on the current character, which also scales with the amount of Kromers thrown away.

3. `/dark_dollars`

Throw away some Dark Dollars for some reason.

4. `/characters`

Delete characters. If there are no characters left, a special different message will be displayed on the API root directory (`/`). Protected by a `password` header for authorization purposes.

5. `/characters_batch`

Delete all characters within the specified `min_level` and `max_level` level limits, inclusive. Protected by a `password` header for authorization purposes.

## Extra Discussion (Possible Future Improvements)

Currently, creating a character takes `O(n)` computing time since we loop through the existing character IDs to check that the input character ID is not a duplicate. For future improvement, we can actually use the `SISMEMBER` command to check if the character ID exists in the existing character IDs set which has a time complexity of `O(1)`. Thus, we can improve the current time needed to create a character.
