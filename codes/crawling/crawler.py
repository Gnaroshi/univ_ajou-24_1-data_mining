import csv
import time
import gc
from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import concurrent.futures

script = """
    var elements = document.querySelectorAll('div[class*="vm-footer"]');
    elements.forEach(function(element) {
        element.parentNode.removeChild(element);
    });
    """
collected_data_cnt = 0
lane = ["top", "jungle", "mid", "adc", "support"]


def close_ads(driver):
    try:
        ad_close_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="closeIconHit"]'))
        )
        scroll_into_view(driver, ad_close_button)
        ad_close_button.click()
    except:
        pass

    try:
        driver.execute_script(script)
    except:
        pass


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def highrankerStatisticCrawer(page, user, start_time):
    print(f"=======| cur user: {user} |========", end="")
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_str = str(timedelta(seconds=execution_time))
    print(f"| time: {execution_time_str} =======|")

    driver = initialize_driver()
    driver.get(f"https://www.op.gg/leaderboards/tier?page={page}")
    driver.implicitly_wait(3)

    data = []
    error_data = []
    error_happened = False
    error_expend_history = 0
    error_get_history = 0

    try:
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f'//*[@id="content-container"]/div[3]/table/tbody/tr[{user}]/td[2]/a',
                )
            )
        )
    except:
        driver.quit()
        return data, error_data, error_happened

    user_a_tag_xpath = driver.find_element(
        By.XPATH,
        f'//*[@id="content-container"]/div[3]/table/tbody/tr[{user}]/td[2]/a',
    )

    user_ID_xpath = driver.find_element(
        By.XPATH,
        f"/html/body/div[1]/div[6]/div[3]/table/tbody/tr[{user}]/td[2]/a/div/span[1]",
    )
    user_ID = user_ID_xpath.text
    user_ID_tag_xpath = driver.find_element(
        By.XPATH,
        f"/html/body/div[1]/div[6]/div[3]/table/tbody/tr[{user}]/td[2]/a/div/span[2]",
    )
    user_ID_tag = user_ID_tag_xpath.text

    scroll_into_view(driver, user_a_tag_xpath)

    current_url = driver.current_url
    limit_cnt = 0
    while True:
        refresh_check = False
        try:
            scroll_into_view(driver, user_a_tag_xpath)
            user_a_tag_xpath.click()
            refresh_check = True
        except:
            driver.refresh()
            close_ads(driver)
        if refresh_check:
            break
        limit_cnt += 1
        if limit_cnt >= 2:
            driver.quit()
            return data, error_data, error_happened
    try:
        WebDriverWait(driver, 5).until(EC.url_changes(current_url))
    except:
        pass

    max_expand = 1
    for expand in range(1, 5):
        close_ads(driver)
        max_expand += 1
        try:
            expand_button_xpath_wait = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="content-container"]/div[2]/button',
                    )
                )
            )
            scroll_into_view(driver, expand_button_xpath_wait)
            expand_button_xpath_wait.click()

        except:
            close_ads(driver)
            error_happened = True
            error_expend_history = expand
            max_expand -= 1

    iter_for_max_expand = max(max_expand * 20 + 1, 0)
    for game in range(1, iter_for_max_expand):

        gt_check = False
        tgt_check = False
        game_type = None
        tgame_type = None

        try:
            game_type_xpath = driver.find_element(
                By.XPATH,
                f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[1]/div[2]/div/div[1]/div[1]/div[1]',
            )
            game_type = game_type_xpath.text
        except:
            gt_check = True
            continue

        try:
            game_type_xpath = driver.find_element(
                By.XPATH,
                f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[1]/div[1]',
            )
            tgame_type = game_type_xpath.text
        except:
            tgt_check = True
            continue

        if not gt_check:
            if game_type != "Ranked Solo":
                continue
        elif not tgt_check:
            if tgame_type != "Ranked Solo":
                continue

        check_xpath = False
        tcheck_xpath = False

        try:
            result_xpath = driver.find_element(
                By.XPATH,
                f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
            )
            result = result_xpath.text
        except:
            check_xpath = True

        try:
            result_xpath = driver.find_element(
                By.XPATH,
                f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
            )
            result = result_xpath.text
        except:
            tcheck_xpath = True

        if tcheck_xpath and check_xpath:
            continue

        our_team = []
        enemy_team = []
        game_players = []
        game_chk = True
        game_time = 0

        if not check_xpath:
            try:
                # game result
                result_xpath = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
                )
                result = result_xpath.text

                # game time
                game_time_xpath = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[1]/div[2]/div/div[1]/div[3]/div[2]",
                )

                game_time_minute = int(game_time_xpath.text.split(" ")[0][0:-1])
                game_time_second = int(game_time_xpath.text.split(" ")[1][0:-1])

                game_time = game_time_minute * 60 + game_time_second

                detail_btn_xpath_wait = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div/div[3]/button",
                        )
                    )
                )
            except:
                continue
            try:
                scroll_into_view(driver, detail_btn_xpath_wait)
                detail_btn_xpath_wait.click()
            except:
                close_ads(driver)
                continue

            our_team_object = []
            our_team_total_kill = -1
            our_team_total_gold = -1
            enemy_team_object = []
            enemy_team_total_kill = -1
            enemy_team_total_gold = -1

            try:
                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text
                    our_champion_lane = player - 1

                    our_champion_name = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[1]/a/div/img",
                    ).get_attribute("alt")

                    our_champion_spell1 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[2]/div[{1}]/img",
                    ).get_attribute("alt")

                    our_champion_spell2 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[2]/div[{2}]/img",
                    ).get_attribute("alt")

                    our_champion_kda = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[6]/div[1]",
                    ).text.split("/")

                    our_champion_kill_cnt = int(our_champion_kda[0])
                    our_champion_death_cnt = int(our_champion_kda[1])
                    our_champion_assist_cnt = int(our_champion_kda[2].split(" ")[0])

                    our_champion_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[7]/div/div[1]/div[1]",
                        ).text.replace(",", "")
                    )

                    our_champion_taken_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[7]/div/div[2]/div[1]",
                        ).text.replace(",", "")
                    )

                    our_champion_wards = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[8]/div/div[1]",
                        ).text
                    )

                    our_champion_cs = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[9]/div[1]",
                        ).text
                    )

                    our_team.append(
                        [
                            our_champion_lane,
                            our_champion_name,
                            our_champion_spell1,
                            our_champion_spell2,
                            our_champion_kill_cnt,
                            our_champion_death_cnt,
                            our_champion_assist_cnt,
                            our_champion_damage,
                            our_champion_taken_damage,
                            our_champion_wards,
                            our_champion_cs,
                        ]
                    )
                    game_players.append(player_name)

                try:
                    our_team_baron = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[1]/div/span[2]",
                        ).text
                    )
                    our_team_dragon = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[2]/div/span[2]",
                        ).text
                    )
                    our_team_riftherald = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[3]/div/span[2]",
                        ).text
                    )
                    our_team_voidgrub = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[4]/div/span[2]",
                        ).text
                    )
                    our_team_tower = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[5]/div/span[2]",
                        ).text
                    )
                    our_team_inhibitor = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[6]/div/span[2]",
                        ).text
                    )
                    our_team_object = [
                        our_team_baron,
                        our_team_dragon,
                        our_team_riftherald,
                        our_team_voidgrub,
                        our_team_tower,
                        our_team_inhibitor,
                    ]

                    our_team_total_kill = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[1]/div/div[{2}]",
                        ).text
                    )

                    our_team_total_gold = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[2]/div/div[{2}]",
                        ).text.replace(",", "")
                    )

                except:
                    our_team_object = [-1 * 6]
                    our_team_total_kill = -1
                    our_team_total_gold = -1
                    print("first our team error")
                    pass

                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text

                    enemy_champion_lane = player - 1

                    enemy_champion_name = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[1]/a/div/img",
                    ).get_attribute("alt")

                    enemy_champion_spell1 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[2]/div[{1}]/img",
                    ).get_attribute("alt")

                    enemy_champion_spell2 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[2]/div[{2}]/img",
                    ).get_attribute("alt")

                    enemy_champion_kda = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[6]/div[1]",
                    ).text.split("/")

                    enemy_champion_kill_cnt = int(enemy_champion_kda[0])
                    enemy_champion_death_cnt = int(enemy_champion_kda[1])
                    enemy_champion_assist_cnt = int(enemy_champion_kda[2].split(" ")[0])

                    enemy_champion_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[7]/div/div[1]/div[1]",
                        ).text.replace(",", "")
                    )

                    enemy_champion_taken_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[7]/div/div[2]/div[1]",
                        ).text.replace(",", "")
                    )

                    enemy_champion_wards = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[8]/div/div[1]",
                        ).text
                    )

                    enemy_champion_cs = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[9]/div[1]",
                        ).text
                    )

                    enemy_team.append(
                        [
                            enemy_champion_lane,
                            enemy_champion_name,
                            enemy_champion_spell1,
                            enemy_champion_spell2,
                            enemy_champion_kill_cnt,
                            enemy_champion_death_cnt,
                            enemy_champion_assist_cnt,
                            enemy_champion_damage,
                            enemy_champion_taken_damage,
                            enemy_champion_wards,
                            enemy_champion_cs,
                        ]
                    )
                    game_players.append(player_name)

                try:
                    enemy_team_baron = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[1]/div/span[2]",
                        ).text
                    )
                    enemy_team_dragon = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[2]/div/span[2]",
                        ).text
                    )
                    enemy_team_riftherald = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[3]/div/span[2]",
                        ).text
                    )
                    enemy_team_voidgrub = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[4]/div/span[2]",
                        ).text
                    )
                    enemy_team_tower = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[5]/div/span[2]",
                        ).text
                    )
                    enemy_team_inhibitor = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[6]/div/span[2]",
                        ).text
                    )
                    enemy_team_object = [
                        enemy_team_baron,
                        enemy_team_dragon,
                        enemy_team_riftherald,
                        enemy_team_voidgrub,
                        enemy_team_tower,
                        enemy_team_inhibitor,
                    ]

                    enemy_team_total_kill = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[1]/div/div[{3}]",
                        ).text
                    )

                    enemy_team_total_gold = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[2]/div/div[{3}]",
                        ).text.replace(",", "")
                    )

                except Exception as e:
                    enemy_team_object = [-1 * 6]
                    enemy_team_total_kill = -1
                    enemy_team_total_gold = -1
                    pass

            except:
                game_chk = False

        elif not tcheck_xpath:
            try:
                # game result
                result_xpath = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
                )
                result = result_xpath.text

                # game time
                game_time_xpath = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[1]/div[2]/div/div[1]/div[3]/div[2]",
                )

                game_time_minute = int(game_time_xpath.text.split(" ")[0][0:-1])
                game_time_second = int(game_time_xpath.text.split(" ")[1][0:-1])

                game_time = game_time_minute * 60 + game_time_second

                # print("game time: ", end="")
                # print(game_time)

                detail_btn_xpath_wait = WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div/div[3]/button",
                        )
                    )
                )
            except:
                continue

            try:
                scroll_into_view(driver, detail_btn_xpath_wait)
                detail_btn_xpath_wait.click()
            except:
                close_ads(driver)
                continue

            try:
                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[1]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text

                    our_champion_lane = player - 1

                    our_champion_name = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[1]/a/div/img",
                    ).get_attribute("alt")

                    our_champion_spell1 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[2]/div[{1}]/img",
                    ).get_attribute("alt")

                    our_champion_spell2 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[2]/div[{2}]/img",
                    ).get_attribute("alt")

                    our_champion_kda = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[6]/div[1]",
                    ).text.split("/")

                    our_champion_kill_cnt = int(our_champion_kda[0])
                    our_champion_death_cnt = int(our_champion_kda[1])
                    our_champion_assist_cnt = int(our_champion_kda[2].split(" ")[0])

                    our_champion_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[7]/div/div[1]/div[1]",
                        ).text.replace(",", "")
                    )

                    our_champion_taken_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[7]/div/div[2]/div[1]",
                        ).text.replace(",", "")
                    )

                    our_champion_wards = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[8]/div/div[1]",
                        ).text
                    )

                    our_champion_cs = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[9]/div[1]",
                        ).text
                    )

                    our_team.append(
                        [
                            our_champion_lane,
                            our_champion_name,
                            our_champion_spell1,
                            our_champion_spell2,
                            our_champion_kill_cnt,
                            our_champion_death_cnt,
                            our_champion_assist_cnt,
                            our_champion_damage,
                            our_champion_taken_damage,
                            our_champion_wards,
                            our_champion_cs,
                        ]
                    )

                    game_players.append(player_name)

                try:
                    our_team_baron = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[1]/div/span[2]",
                        ).text
                    )
                    our_team_dragon = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[2]/div/span[2]",
                        ).text
                    )
                    our_team_riftherald = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[3]/div/span[2]",
                        ).text
                    )
                    our_team_voidgrub = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[4]/div/span[2]",
                        ).text
                    )
                    our_team_tower = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[5]/div/span[2]",
                        ).text
                    )
                    our_team_inhibitor = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{1}]/ul/li[6]/div/span[2]",
                        ).text
                    )
                    our_team_object = [
                        our_team_baron,
                        our_team_dragon,
                        our_team_riftherald,
                        our_team_voidgrub,
                        our_team_tower,
                        our_team_inhibitor,
                    ]

                    our_team_total_kill = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[1]/div/div[{2}]",
                        ).text
                    )

                    our_team_total_gold = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[2]/div/div[{2}]",
                        ).text.replace(",", "")
                    )

                except:
                    our_team_object = [-1 * 6]
                    our_team_total_kill = -1
                    our_team_total_gold = -1
                    pass

                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text

                    enemy_champion_lane = player - 1

                    enemy_champion_name = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[1]/a/div/img",
                    ).get_attribute("alt")

                    enemy_champion_spell1 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[2]/div[{1}]/img",
                    ).get_attribute("alt")

                    enemy_champion_spell2 = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[2]/div[{2}]/img",
                    ).get_attribute("alt")

                    enemy_champion_kda = driver.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[6]/div[1]",
                    ).text.split("/")

                    enemy_champion_kill_cnt = int(enemy_champion_kda[0])
                    enemy_champion_death_cnt = int(enemy_champion_kda[1])
                    enemy_champion_assist_cnt = int(enemy_champion_kda[2].split(" ")[0])

                    enemy_champion_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[7]/div/div[1]/div[1]",
                        ).text.replace(",", "")
                    )

                    enemy_champion_taken_damage = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[7]/div/div[2]/div[1]",
                        ).text.replace(",", "")
                    )

                    enemy_champion_wards = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[8]/div/div[1]",
                        ).text
                    )

                    enemy_champion_cs = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[9]/div[1]",
                        ).text
                    )

                    enemy_team.append(
                        [
                            enemy_champion_lane,
                            enemy_champion_name,
                            enemy_champion_spell1,
                            enemy_champion_spell2,
                            enemy_champion_kill_cnt,
                            enemy_champion_death_cnt,
                            enemy_champion_assist_cnt,
                            enemy_champion_damage,
                            enemy_champion_taken_damage,
                            enemy_champion_wards,
                            enemy_champion_cs,
                        ]
                    )

                    game_players.append(player_name)

                try:
                    enemy_team_baron = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[1]/div/span[2]",
                        ).text
                    )
                    enemy_team_dragon = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[2]/div/span[2]",
                        ).text
                    )
                    enemy_team_riftherald = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[3]/div/span[2]",
                        ).text
                    )
                    enemy_team_voidgrub = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[4]/div/span[2]",
                        ).text
                    )
                    enemy_team_tower = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[5]/div/span[2]",
                        ).text
                    )
                    enemy_team_inhibitor = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[{3}]/ul/li[6]/div/span[2]",
                        ).text
                    )
                    enemy_team_object = [
                        enemy_team_baron,
                        enemy_team_dragon,
                        enemy_team_riftherald,
                        enemy_team_voidgrub,
                        enemy_team_tower,
                        enemy_team_inhibitor,
                    ]

                    enemy_team_total_kill = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[1]/div/div[{3}]",
                        ).text
                    )

                    enemy_team_total_gold = int(
                        driver.find_element(
                            By.XPATH,
                            f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div[2]/div[1]/div/div[2]/div[2]/div/div[{3}]",
                        ).text.replace(",", "")
                    )

                except:
                    enemy_team_object = [-1 * 6]
                    enemy_team_total_kill = -1
                    enemy_team_total_gold = -1
                    pass

            except:
                game_chk = False

        if game_chk:
            if result[0] == "V" or result[0] == "D":
                if result[0] == "V":
                    result_value = 1
                elif result[0] == "D":
                    result_value = 0
                data.append(
                    [
                        user_ID,
                        user_ID_tag,
                        result_value,
                        game_time,
                        our_team,
                        our_team_object,
                        our_team_total_kill,
                        our_team_total_gold,
                        enemy_team,
                        enemy_team_object,
                        enemy_team_total_kill,
                        enemy_team_total_gold,
                        game_players,
                    ]
                )
                scroll_into_view(driver, detail_btn_xpath_wait)
                detail_btn_xpath_wait.click()

        if error_happened:
            error_data.append(
                [user_ID, user_ID_tag, error_expend_history, error_get_history]
            )

    driver.quit()
    return data, error_data, error_happened


def initialize_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


# def process_user_batch(
#     page, start_user, end_user, csv_file, csv_file_error, start_time
# ):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         futures = []
#         for user in range(start_user, end_user + 1):
#             futures.append(executor.submit(highrankerStatisticCrawer, page, user))

#         for future in concurrent.futures.as_completed(futures):
#             try:
#                 (
#                     one_user_statistic,
#                     one_user_statistic_error,
#                     one_user_statistic_error_happened,
#                 ) = future.result()
#                 with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
#                     writer = csv.writer(file)
#                     writer.writerows(one_user_statistic)

#                 if one_user_statistic_error_happened:
#                     with open(
#                         csv_file_error, mode="a", newline="", encoding="utf-8"
#                     ) as file:
#                         writer = csv.writer(file)
#                         writer.writerows(one_user_statistic_error)
#             except Exception as e:
#                 print(f"Error processing user: {e}")

#             gc.collect()


def process_user_batch(
    page, start_user, end_user, csv_file, csv_file_error, start_time
):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for user in range(start_user, end_user + 1):
            futures.append(
                executor.submit(highrankerStatisticCrawer, page, user, start_time)
            )

        for future in concurrent.futures.as_completed(futures):
            try:
                (
                    one_user_statistic,
                    one_user_statistic_error,
                    one_user_statistic_error_happened,
                ) = future.result()
                with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(one_user_statistic)

                if one_user_statistic_error_happened:
                    with open(
                        csv_file_error, mode="a", newline="", encoding="utf-8"
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerows(one_user_statistic_error)
            except Exception as e:
                print(f"Error processing user: {e}")

            gc.collect()


def process_page_batch(page, csv_file, csv_file_error, start_time):
    user_batch_size = 25
    processes = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # for user_batch_start in range(1, 101, user_batch_size):
        #     user_batch_end = min(user_batch_start + user_batch_size - 1, 100)
        #     processes.append(
        #         executor.submit(
        #             process_user_batch,
        #             page,
        #             user_batch_start,
        #             user_batch_end,
        #             csv_file,
        #             csv_file_error,
        #             start_time,
        #         )
        #     )
        st = 1
        if page == 8:
            st = 20
        for user_batch_start in range(st, 101, user_batch_size):
            user_batch_end = min(user_batch_start + user_batch_size - 1, 100)
            processes.append(
                executor.submit(
                    process_user_batch,
                    page,
                    user_batch_start,
                    user_batch_end,
                    csv_file,
                    csv_file_error,
                    start_time,
                )
            )
        for process in concurrent.futures.as_completed(processes):
            process.result()


if __name__ == "__main__":
    start_time = time.time()
    start_time_for_csv = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_file = "A" + start_time_for_csv + ".csv"
    csv_file_error = "B" + start_time_for_csv + ".csv"

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "user_ID",
                "user_ID_tag",
                "result_value",
                "game_time",
                "our_team",
                "our_team_object",
                "our_team_total_kill",
                "our_team_total_gold",
                "enemy_team",
                "enemy_team_object",
                "enemy_team_total_kill",
                "enemy_team_total_gold",
                "game_players",
            ]
        )

    with open(csv_file_error, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["user_ID", "user_ID_tag", "error_expend_history", "error_get_history"]
        )

    for page in range(8, 11):
        print(f"=======| cur page: {page} |========")
        process_page_batch(page, csv_file, csv_file_error, start_time)

    print("-------| end |-------")
