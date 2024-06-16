import csv
import time
import gc
from datetime import timedelta
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import concurrent.futures

import pandas as pd

script = """
    var elements = document.querySelectorAll('div[class*="vm-footer"]');
    elements.forEach(function(element) {
        element.parentNode.removeChild(element);
    });
    """
collected_data_cnt = 0


def close_ads(driver):
    try:
        ad_close_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="closeIconHit"]'))
        )
        ad_close_button.click()
    # except Exception as e:
    except:
        pass

    try:
        driver.execute_script(script)
    # except Exception as e:
    except:
        pass


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def highrankerStatisticCrawer(driver, cur_user):
    # if cur_user % 10 == 1:
    print(f"=======| cur user: {cur_user} |========", end="")
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_str = str(timedelta(seconds=execution_time))
    print(f"| time: {execution_time_str} =======|")

    data = []
    error_data = []
    error_happened = False
    error_expend_history = 0
    error_get_history = 0

    # user history link
    try:
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f'//*[@id="content-container"]/div[3]/table/tbody/tr[{cur_user}]/td[2]/a',
                )
            )
        )
    except:
        driver.refresh()
        return data, error_data, error_happened

    user_a_tag_xpath = driver.find_element(
        By.XPATH,
        f'//*[@id="content-container"]/div[3]/table/tbody/tr[{cur_user}]/td[2]/a',
    )
    # user_a_tag_xpath.click()

    user_ID_xpath = driver.find_element(
        By.XPATH,
        f"/html/body/div[1]/div[6]/div[3]/table/tbody/tr[{cur_user}]/td[2]/a/div/span[1]",
    )
    user_ID = user_ID_xpath.text
    user_ID_tag_xpath = driver.find_element(
        By.XPATH,
        f"/html/body/div[1]/div[6]/div[3]/table/tbody/tr[{cur_user}]/td[2]/a/div/span[2]",
    )
    user_ID_tag = user_ID_tag_xpath.text

    scroll_into_view(driver, user_a_tag_xpath)

    current_url = driver.current_url
    limit_cnt = 0
    while True:
        refresh_check = False
        try:
            user_a_tag_xpath.click()
            refresh_check = True
        except:
            driver.refresh()
            close_ads(driver)
        if refresh_check == True:
            break
        limit_cnt += 1
        if limit_cnt >= 5:
            return data, error_data, error_happened
    try:
        WebDriverWait(driver, 5).until(EC.url_changes(current_url))
    except:
        pass

    # TODO change range for crawling
    max_expand = 1
    # for expand in range(1, 5):
    for expand in range(1, 3):
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
            expand_button_xpath_wait.click()

            # TODO
            # if expand != 3:
            if expand != 5:
                WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//*[@id="content-container"]/div[2]/button')
                    )
                )

        except Exception as e:
            print(f"Error on expand {expand}")
            close_ads(driver)
            error_happened = True
            error_expend_history = expand
            max_expand -= 1

    # TODO
    # for game in range(1, 101):
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

        if gt_check == False:
            if game_type != "Ranked Solo":
                continue
        elif tgt_check == False:
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
        except Exception as e:
            check_xpath = True

        try:
            result_xpath = driver.find_element(
                By.XPATH,
                f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
            )
            result = result_xpath.text
        except Exception as e:
            tcheck_xpath = True

        if tcheck_xpath and check_xpath:
            continue
            # return data, error_data, error_happened

        ourteam_champions_with_spell = []
        enemy_champions_with_spell = []
        game_players = []
        game_chk = True

        if check_xpath == False:
            try:
                result_xpath = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[10]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
                )
                result = result_xpath.text

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

            try:
                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{1}]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text
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
                    ourteam_champions_with_spell_one = [
                        our_champion_name,
                        our_champion_spell1,
                        our_champion_spell2,
                    ]

                    game_players.append(player_name)
                    ourteam_champions_with_spell.append(
                        ourteam_champions_with_spell_one
                    )

                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text
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
                    enemy_champions_with_spell_one = [
                        enemy_champion_name,
                        enemy_champion_spell1,
                        enemy_champion_spell2,
                    ]
                    game_players.append(player_name)
                    enemy_champions_with_spell.append(enemy_champions_with_spell_one)
            except:
                game_chk = False

        elif tcheck_xpath == False:
            try:
                result_xpath = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[9]/div[2]/div[3]/div[{game}]/div/div[2]/div/div[1]/div[3]/div[1]",
                )
                result = result_xpath.text

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
                    ourteam_champions_with_spell_one = [
                        our_champion_name,
                        our_champion_spell1,
                        our_champion_spell2,
                    ]
                    game_players.append(player_name)
                    ourteam_champions_with_spell.append(
                        ourteam_champions_with_spell_one
                    )

                for player in range(1, 6):
                    player_name = driver.find_element(
                        By.XPATH,
                        f'//*[@id="content-container"]/div[2]/div[3]/div[{game}]/div[2]/div[1]/table[{2}]/tbody/tr[{player}]/td[4]/div[1]/a/div/span',
                    ).text
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
                    enemy_champions_with_spell_one = [
                        enemy_champion_name,
                        enemy_champion_spell1,
                        enemy_champion_spell2,
                    ]
                    game_players.append(player_name)
                    enemy_champions_with_spell.append(enemy_champions_with_spell_one)
            except:
                game_chk = False

        if game_chk == True:
            result_value = 0
            if result[0] == "V":
                result_value = 1
            data.append(
                [
                    user_ID,
                    user_ID_tag,
                    result_value,
                    ourteam_champions_with_spell,
                    enemy_champions_with_spell,
                    game_players,
                ]
            )
            detail_btn_xpath_wait.click()

        if error_happened == True:
            error_data.append(
                [user_ID, user_ID_tag, error_expend_history, error_get_history]
            )

    driver.back()

    return data, error_data, error_happened


if __name__ == "__main__":
    start_time = time.time()
    start_time_for_csv = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_file = "A" + start_time_for_csv + ".csv"
    csv_file_error = "B" + start_time_for_csv + ".csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "#",
                "user_ID",
                "user_ID_tag",
                "result_value",
                "ourteam_champions_with_spell",
                "enemy_champions_with_spell",
                "game_players",
            ]
        )
    with open(csv_file_error, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "user_ID",
                "user_ID_tag",
                "error_expend_history",
                "error_get_history",
            ]
        )

    statistics_highrank_url = "https://www.op.gg/leaderboards/tier"
    statistics_highrank_data = []
    statistics_highrank_data_error = []
    statistics_highrank_data_error_happened = False

    driver = webdriver.Chrome()
    driver.get(statistics_highrank_url)
    driver.implicitly_wait(3)

    # TODO
    # for page in range(1, 4):
    for page in range(1, 11):
        print(f"=======| cur page: {page} |========")
        close_ads(driver)
        try:
            if page != 1:
                current_url = driver.current_url
                next_page_tag = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"/html/body/div[1]/div[6]/div[3]/div/div/div[2]/a[{page}]",
                        )
                    )
                )
                next_page_tag.click()
                WebDriverWait(driver, 5).until(EC.url_changes(current_url))
        except:
            continue

        # for user in range(1, 101):
        for user in range(1, 51):
            (
                one_user_statistic,
                one_user_statistic_error,
                one_user_statistic_error_happened,
            ) = highrankerStatisticCrawer(driver, user)

            collected_data_cnt += len(one_user_statistic)
            print(f"#######| data counts: {collected_data_cnt} |#######")
            for temp_data in one_user_statistic:
                with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(temp_data)

            if one_user_statistic_error_happened == True:
                statistics_highrank_data_error_happened = True
                for temp_data in one_user_statistic_error:
                    with open(
                        csv_file_error, mode="a", newline="", encoding="utf-8"
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerow(temp_data)

        gc.collect()
    # df = pd.DataFrame(statistics_highrank_data)
    # df.to_csv("AAAOP_GG_Data_" + "statistics_highrank" + ".csv", encoding="utf-8-sig")

    # if statistics_highrank_data_error_happened == True:
    #     df_error = pd.DataFrame(statistics_highrank_data_error)
    #     df_error.to_csv(
    #         "AEEOP_GG_Data_" + "statistics_highrank" + ".csv", encoding="utf-8-sig"
    #     )

    print("-------| end |-------")
    driver.quit()
