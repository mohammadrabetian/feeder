This project uses GraphQL for Apis and GraphQL spec is pretty much self documented, 
this file is just for you to have a quick run and see what queries you could run on this project...

After running the application go to http://localhost:8000/graphql/ 

#### Register a user
```graphql
mutation RegisterUser {
  register(registerInfo: {username:"Eike", password: "testing321"}) {
    success
  }
}
```
#### Logout
```graphql
mutation Logout {
  logout{
    success
  }
}
```
#### Login
```graphql
mutation Login {
  login(username: "Eike", password: "testing321") {
    success
    username
  }
}
```
#### Register a feed
```graphql
mutation RegisterFeed {
  registerFeed(url: "http://www.nu.nl/rss/Algemeen") {
    feed {
      uuid
    }
  }
}
```
#### Updating a feed
* You should provide uuid of the feed you're wishing to update
```graphql
mutation UpdateFeed {
  updateFeed(uuid: "430c8f45-f74f-4e52-95a0-1cfe40f3bd9c") {
    success
  }
}
```
#### Check update state of a feed
* Could be used with a simple polling method to know the state of feed updates
* Gets a feed uuid
* The value expires in 30 seconds
```graphql
query FeedUpdateState {
	updateState(uuid: "7c70fdc4-cca5-40e8-bbc5-e5fc2b3fb4e5")
}
```
#### Delete a feed
```graphql
mutation DeleteFeed {
  deleteFeed(uuid: "31615f7a-350a-4c6e-9bf8-811fcef583b5") {
    success
  }
}
```
#### Query Feeds
* Supports filters
* orders by feed lastUpdated
* Supports pagination
```graphql
query Feeds {
  feeds {
    edges {
      node {
        uuid
        user{
          username
        }
        title
        subtitle
        rights
        url
        lastUpdated
        info
        language
      }
    }
  }
}
```
#### Query Feed Items
* Supports filters
* orders by feed lastUpdated
* Supports pagination
```graphql
query FeedItems {
  feedItems {
    edges {
      node {
        uuid
        title
        dateModified
        content
        feed {
          uuid
          url
          title
        }
      }
    }
  }
}
```

#### Read an Item
```graphql
mutation ReadItem {
  readFeedItem(uuid: "8a716c4e-7558-4628-8c48-38ac9ee7b23f") {
    success
  }
}
```

#### Unread an Item
```graphql
mutation UnReadItem {
  unreadFeedItem(uuid: "8a716c4e-7558-4628-8c48-38ac9ee7b23f") {
    success
  }
}
```