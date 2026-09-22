from fastapi import APIRouter, HTTPException,  status, Depends
from promptune.services.subsonic import SubsonicClient, SubsonicLoginDTO, create_subsonic_client
from httpx import RequestError
from promptune.db.models.users import auth_cookie, get_jwt_strategy, current_active_user, User
from promptune.db.dao.user_dao import UserDAO
from promptune.db.dao.music_dao import MusicLibraryDAO
router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload:SubsonicLoginDTO, user_dao:UserDAO = Depends() ):
    client = SubsonicClient.from_password(
        payload.server_url,
        payload.username,
        payload.password
        )
    try:
        is_valid = await client.ping()

    except RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not connect to subsonic server. {e}"
        )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Check if user already exists 
    print("make query")
    user = await user_dao.get_by_username(payload.username)
    print(user)
    if user:
        if payload.username == user.subsonic_username:
            print("exists")
            jwt_strategy = get_jwt_strategy()
            return await auth_cookie.login(jwt_strategy, user)
    # Create new user
    else:
        print("adding user")
        return await user_dao.create_user(
            server_url=payload.server_url,
            username=payload.username,
            token=client.token,
            salt=client.salt,
            email=f"{payload.username}@{payload.server_url.replace("http://","").replace("https://", "")}",
            hashed_password="NOT_USED"
            )

@router.get("/artists")   
async def get_artists(
    client: SubsonicClient = Depends(create_subsonic_client) 
    ):

    return await client.get_artists()

@router.get("/albums")
async def get_albums(
    client: SubsonicClient = Depends(create_subsonic_client) 
    ):

    return await client.get_albums()

@router.get("/tracks")
async def get_tracks(
    client: SubsonicClient = Depends(create_subsonic_client)
    ):

    return await client.get_tracks()

@router.post("/sync")
async def sync(
    client: SubsonicClient = Depends(create_subsonic_client),
    music_dao: MusicLibraryDAO = Depends()
    ):

    artists = await client.get_artists()
    albums = await client.get_albums()
    tracks = await client.get_tracks()

    await music_dao.clear_library()

    await music_dao.insert_artists(artist_data=artists)
    await music_dao.insert_albums(album_data=albums)
    await music_dao.insert_tracks(tracks_data=tracks)
    
    
    
    

        

       