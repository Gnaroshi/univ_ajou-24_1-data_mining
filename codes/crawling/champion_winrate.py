from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def championStatCrawl(champion_rank):
    champion_name_xpath = '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[2]'
    champion_name_tag = champion_name_xpath.format(champion_rank)
    champion_name = driver.find_element(By.XPATH, champion_name_tag).text

    champion_play_xpath = '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[3]'
    champion_play_tag = champion_play_xpath.format(champion_rank)
    champion_play = driver.find_element(By.XPATH, champion_play_tag).text

    champion_rate_xpath = (
        '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[4]/span'
    )
    champion_rate_tag = champion_rate_xpath.format(champion_rank)
    champion_rate = driver.find_element(By.XPATH, champion_rate_tag).text

    champion_win_rate_xpath = (
        '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[5]/div/div[2]'
    )
    champion_win_rate_tag = champion_win_rate_xpath.format(champion_rank)
    champion_win_rate = driver.find_element(By.XPATH, champion_win_rate_tag).text

    champion_pick_rate_xpath = (
        '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[6]/div/div[2]'
    )
    champion_pick_rate_tag = champion_pick_rate_xpath.format(champion_rank)
    champion_pick_rate = driver.find_element(By.XPATH, champion_pick_rate_tag).text

    champion_ban_rate_xpath = (
        '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[7]'
    )
    champion_ban_rate_tag = champion_ban_rate_xpath.format(champion_rank)
    champion_ban_rate = driver.find_element(By.XPATH, champion_ban_rate_tag).text

    champion_cs_xpath = '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[8]'
    champion_cs_tag = champion_cs_xpath.format(champion_rank)
    champion_cs = driver.find_element(By.XPATH, champion_cs_tag).text

    champion_gold_xpath = '//*[@id="content-container"]/div[2]/table/tbody/tr[{}]/td[9]'
    champion_gold_tag = champion_gold_xpath.format(champion_rank)
    champion_gold = driver.find_element(By.XPATH, champion_gold_tag).text

    data = {
        "#": champion_rank,
        "챔피언": champion_name,
        "플레이 수": champion_play,
        "평점": champion_rate,
        "승률": champion_win_rate,
        "게임당 픽률": champion_pick_rate,
        "게임당 밴률": champion_ban_rate,
        "cs": champion_cs,
        "gold": champion_gold,
    }

    return data


if __name__ == "__main__":
    positions = ["top", "jungle", "mid", "adc", "support"]
    statistics_champion_url = "https://www.op.gg/statistics/champions"
    for lane in positions:
        driver = webdriver.Chrome()
        driver.get(statistics_champion_url + "?position=" + lane)

        champion_data = []

        for i in range(1, 163):
            champion_data.append(championStatCrawl(i))

        df = pd.DataFrame(champion_data)
        df.to_csv("OP_GG_Data_" + lane + ".csv", encoding="utf-8-sig")
